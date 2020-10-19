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
from mcs_benchmark_data.models.benchmark_hypothesis import BenchmarkHypothesis
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_goal import BenchmarkGoal
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample


class PhysicalIQaBenchmarkTransformer(_Transformer):

    __URI_BASE = "benchmark:physicaliqa"
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

            if dataset_type != "test":
                yield from self.__transform_benchmark_sample(
                    kwds[dataset_type + "_jsonl_file_path"],
                    kwds[dataset_type + "_labels_file_path"],
                    dataset_type,
                    new_dataset.uri,
                )
            else:
                yield from self.__transform_benchmark_sample(
                    kwds[dataset_type + "_jsonl_file_path"],
                    None,
                    dataset_type,
                    new_dataset.uri,
                )

    def __transform_benchmark_sample(
        self,
        sample_jsonl_file_path,
        sample_labels_file_path,
        sample_type: str,
        dataset_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        with open(sample_labels_file_path) as sample_labels:
            all_labels = list(sample_labels)

        with open(sample_jsonl_file_path) as sample_jsonl:
            all_samples = list(sample_jsonl)

        i = 0

        for line in all_samples:

            sample = json.loads(line)

            correct_choice = None

            if sample_type != "test":
                correct_choice = URIRef(
                    f"{dataset_uri}:sample:{sample['id']}:hypothesis:{int(all_labels[i]) + 1}"
                )

            benchmark_sample = BenchmarkSample(
                uri=URIRef(f"{dataset_uri}:sample:{sample['id']}"),
                dataset_uri=dataset_uri,
                correct_choice=correct_choice,
            )

            yield benchmark_sample

            question_type = BenchmarkQuestionType.multiple_choice(
                uri_base=self.__URI_BASE,
                benchmark_sample_uri=benchmark_sample.uri,
            )
            yield question_type

            goal = BenchmarkGoal(
                uri=URIRef(f"{benchmark_sample.uri}:goal"),
                benchmark_sample_uri=benchmark_sample.uri,
                text=sample["goal"],
            )

            yield goal

            sol1 = BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample.uri}:hypothesis:1"),
                benchmark_sample_uri=benchmark_sample.uri,
                position=1,
                text=sample["sol1"],
            )

            yield sol1

            sol2 = BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample.uri}:hypothesis:2"),
                benchmark_sample_uri=benchmark_sample.uri,
                position=1,
                text=sample["sol2"],
            )

            yield sol2

            i += 1
