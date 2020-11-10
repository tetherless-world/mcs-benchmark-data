import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.dataset_type import DatasetType


class PhysicalIQaBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        all_labels = None

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = (
                self._extracted_data_dir_path
                / "datasets"
                / dataset_type
                / f"{dataset_type}_labels.lst"
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = (
            self._extracted_data_dir_path
            / "datasets"
            / dataset_type
            / f"{dataset_type}_samples.jsonl"
        )

        for i, sample in enumerate(self._read_jsonl_file(sample_jsonl_file_path)):

            sample_id = sample["id"]

            benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample_id}")

            correct_choice = None

            if dataset_type != DatasetType.TEST.value:
                correct_choice = URIRef(
                    f"{benchmark_sample_uri}:correct_choice:{int(all_labels[i]) + 1}"
                )

            yield BenchmarkQuestionType.multiple_choice(
                uri_base=self._uri_base,
                benchmark_sample_uri=benchmark_sample_uri,
            )

            yield from self._yield_sample_concept_context(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                concepts=None,
                context=None,
                correct_choice=correct_choice,
            )

            yield from self._yield_goal_models(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                benchmark_sample_uri=benchmark_sample_uri,
                goal=sample["goal"],
                solutions=tuple((sample["sol1"], sample["sol2"])),
            )