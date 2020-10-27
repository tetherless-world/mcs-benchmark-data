import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef
from dataclasses_json import dataclass_json

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _Benchmark_Transformer
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


class PhysicalIQaBenchmarkTransformer(_Benchmark_Transformer):
    def transform(self, **kwds) -> Generator[_Model, None, None]:

        yield from _Benchmark_Transformer._transform(self, **kwds)

    def _transform_benchmark_sample(
        self, dataset_type: str, dataset_uri: URIRef, **kwds
    ) -> Generator[_Model, None, None]:

        if dataset_type != "test":
            sample_labels_file_path = kwds["extracted_path"] / getattr(
                kwds["file_names"], dataset_type + "_labels"
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = kwds["extracted_path"] / getattr(
            kwds["file_names"], dataset_type + "_samples"
        )

        with open(sample_jsonl_file_path) as sample_file:
            all_samples = list(sample_file)

        i = 0

        for line in all_samples:

            sample = json.loads(line)

            benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample['id']}")

            correct_choice = None

            if dataset_type != "test":
                correct_choice = int(all_labels[i]) + 1

            yield from _Benchmark_Transformer._prepare_sample(
                self,
                dataset_type=dataset_type,
                dataset_uri=dataset_uri,
                sample=sample,
                correct_choice=correct_choice,
            )

            yield BenchmarkGoal(
                uri=URIRef(f"{benchmark_sample_uri}:goal"),
                benchmark_sample_uri=benchmark_sample_uri,
                text=sample["goal"],
            )

            yield BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample_uri}:hypothesis:1"),
                benchmark_sample_uri=benchmark_sample_uri,
                position=1,
                text=sample["sol1"],
            )

            yield BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample_uri}:hypothesis:2"),
                benchmark_sample_uri=benchmark_sample_uri,
                position=1,
                text=sample["sol2"],
            )

            i += 1
