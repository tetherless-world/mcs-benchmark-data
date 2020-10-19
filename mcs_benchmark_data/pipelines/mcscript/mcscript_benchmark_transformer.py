import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef
from dataclasses_json import dataclass_json

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_bootstrap import BenchmarkBootstrap
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample


class MCScriptBenchmarkTransformer(_Transformer):

    __URI_BASE = "benchmark:mcscript"
    __BENCHMARK_DATASET_CLASSES = {
        "dev": BenchmarkDevDataset,
        "test": BenchmarkTestDataset,
        "train": BenchmarkTrainDataset,
    }

    def transform(
        self, benchmark_json_file_path: Path, **kwds
    ) -> Generator[_Model, None, None]:

        with open(benchmark_json_file_path) as benchmark_json:
            benchmark_metadata = json.loads(benchmark_json.read())

        benchmark_bootstrap = BenchmarkBootstrap.from_dict(benchmark_metadata)

        benchmark = Benchmark(
            uri=URIRef(f"{self.__URI_BASE}:benchmark:{benchmark_metadata['@id']}"),
            name=benchmark_bootstrap.name,
            abstract=benchmark_bootstrap.abstract,
            authors=tuple(author["name"] for author in benchmark_bootstrap.authors),
        )

        yield benchmark

        for dataset in benchmark_metadata["datasets"]:

            dataset_type = dataset["@id"].split("/")[-1]

            dataset_uri = URIRef(f"{self.__URI_BASE}:dataset:{dataset['@id']}")

            new_dataset = self.__BENCHMARK_DATASET_CLASSES[dataset_type](
                uri=dataset_uri, benchmark_uri=benchmark.uri, name=dataset["name"]
            )

            yield new_dataset

            yield from self.__transform_benchmark_sample(
                kwds[dataset_type + "_json_file_path"], dataset_type, new_dataset.uri
            )

    def __transform_benchmark_sample(
        self, sample_json_file_path, sample_type: str, dataset_uri: URIRef
    ) -> Generator[_Model, None, None]:

        with open(sample_json_file_path) as sample_json:
            all_samples = json.load(sample_json)

        sample_dict = all_samples["data"]["instance"]

        for sample in sample_dict:

            correct_choice = None

            benchmark_sample = BenchmarkSample(
                uri=URIRef(f"{dataset_uri}:sample:{sample['@id']}"),
                dataset_uri=dataset_uri,
                correct_choice=correct_choice,
            )

            yield benchmark_sample

            concept = BenchmarkConcept(
                uri=URIRef(f"{benchmark_sample.uri}:concept"),
                benchmark_sample_uri=benchmark_sample.uri,
                concept=sample["@scenario"],
            )

            yield concept

            context = BenchmarkContext(
                uri=URIRef(f"{benchmark_sample.uri}:context"),
                benchmark_sample_uri=benchmark_sample.uri,
                text=sample["text"],
            )

            yield context

            question_type = BenchmarkQuestionType.multiple_choice(
                uri_base=self.__URI_BASE,
                benchmark_sample_uri=benchmark_sample.uri,
            )

            yield question_type

            if sample["questions"]:

                for question in sample["questions"]["question"]:
                    if isinstance(question, dict):
                        benchmark_question = BenchmarkQuestion(
                            uri=URIRef(
                                f"{benchmark_sample.uri}:question:{question['@id']}"
                            ),
                            benchmark_sample_uri=benchmark_sample.uri,
                            text=question["@text"],
                        )

                        yield benchmark_question

                        for answer in question["answer"]:
                            benchmark_answer = BenchmarkAnswer(
                                uri=URIRef(
                                    f"{benchmark_question.uri}:choice:{str(answer['@id'])}"
                                ),
                                benchmark_sample_uri=benchmark_sample.uri,
                                position=answer["@id"],
                                text=answer["@text"],
                            )

                            yield benchmark_answer

                            if answer["@correct"] == "True":
                                correct_choice = URIRef(
                                    f"{benchmark_question.uri}:correct_choice:{answer['@id']}"
                                )
