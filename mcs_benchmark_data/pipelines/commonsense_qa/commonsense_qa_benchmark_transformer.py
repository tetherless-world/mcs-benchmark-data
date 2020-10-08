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
from mcs_benchmark_data.models.benchmark_antecedent import BenchmarkAntecedent
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample


class CommonsenseQaBenchmarkTransformer(_Transformer):

    __URI_BASE = "benchmark:commonsense_qa"
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
            uri=URIRef(
                "{}:benchmark:{}".format(self.__URI_BASE, benchmark_metadata["@id"])
            ),
            name=benchmark_bootstrap.name,
            abstract=benchmark_bootstrap.abstract,
            authors=tuple(author["name"] for author in benchmark_bootstrap.authors),
        )

        yield benchmark

        for dataset in benchmark_metadata["datasets"]:

            dataset_type = dataset["@id"].split("/")[-1]

            dataset_uri = URIRef(
                "{}:dataset:{}".format(self.__URI_BASE, dataset["@id"])
            )

            new_dataset = self.__BENCHMARK_DATASET_CLASSES[dataset_type](
                uri=dataset_uri, benchmark_uri=benchmark.uri, name=dataset["name"]
            )

            yield new_dataset

            yield from self.__transform_benchmark_sample(
                kwds[dataset_type + "_jsonl_file_path"], dataset_type, new_dataset.uri
            )

    def __transform_benchmark_sample(
        self, sample_jsonl_file_path, sample_type: str, dataset_uri: URIRef
    ) -> Generator[_Model, None, None]:

        with open(sample_jsonl_file_path) as sample_jsonl:
            all_samples = list(sample_jsonl)

        question_type = BenchmarkQuestionType.MULTIPLE_CHOICE
        question_category = None

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        for line in all_samples:

            sample = json.loads(line)

            correct_choice = None

            if sample_type != "test":
                correct_choice = ans_mapping[sample["answerKey"]]

            benchmark_sample = BenchmarkSample(
                uri=URIRef("{}:sample:{}".format(dataset_uri, sample["id"])),
                dataset_uri=dataset_uri,
                question_type=question_type,
                question_category=question_category,
                correct_choice=correct_choice,
            )

            yield benchmark_sample

            concept = BenchmarkConcept(
                uri=URIRef("{}:concept".format(benchmark_sample.uri)),
                benchmark_sample_uri=benchmark_sample.uri,
                concept=sample["question"]["question_concept"],
            )

            yield concept

            choices_list = []

            for item in sample["question"]["choices"]:
                choice = BenchmarkAnswer(
                    uri=URIRef(
                        "{}:choice:{}".format(benchmark_sample.uri, item["label"])
                    ),
                    position=item["label"],
                    text=item["text"],
                )
                choices_list.append(choice)

                yield choice

            # Choices seems redundant now. Need to check-in about this.
            # choices = BenchmarkChoices(
            #     benchmark_sample_uri=benchmark_sample.uri,
            #     choices=tuple(choices_list),
            # )

            # yield choices

            antecedent = BenchmarkAntecedent(
                uri=URIRef("{}:antecedent".format(benchmark_sample.uri)),
                benchmark_sample_uri=benchmark_sample.uri,
            )

            yield antecedent

            question = BenchmarkQuestion(
                uri=URIRef("{}:question".format(benchmark_sample.uri)),
                antecedent_uri=antecedent.uri,
                text=sample["question"]["stem"],
            )

            yield question
