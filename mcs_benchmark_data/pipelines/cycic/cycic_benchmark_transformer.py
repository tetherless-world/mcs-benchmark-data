import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class CycicBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        all_labels = None

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = (
                self._pipeline_data_dir_path
                / "datasets"
                / dataset_type
                / f"{dataset_type}_labels.jsonl"
            )

            all_labels = self._read_jsonl_file(sample_labels_file_path)

        sample_jsonl_file_path = (
            self._pipeline_data_dir_path
            / "datasets"
            / dataset_type
            / f"{dataset_type}_samples.jsonl"
        )

        for sample in self._read_jsonl_file(sample_jsonl_file_path):

            label_entry = next(all_labels)

            sample_id = f"{sample['run_id']}_{sample['guid']}"

            benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample_id}")

            correct_choice = None

            if dataset_type != DatasetType.TEST.value:
                correct_choice = URIRef(
                    f"{dataset_uri}:sample:{sample_id}:correct_choice:{label_entry['correct_answer']}"
                )

            yield BenchmarkQuestionType.multiple_choice(
                uri_base=self._uri_base,
                benchmark_sample_uri=benchmark_sample_uri,
            )

            letters = ["A", "B", "C", "D", "E"]

            answer_num = 0

            while f"answer_option{answer_num}" in sample:
                answer_num += 1

            yield from self._yield_sample_concept_context(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                concepts=sample["categories"],
                context=None,
                correct_choice=correct_choice,
            )

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                benchmark_sample_uri=benchmark_sample_uri,
                question=sample["question"],
                answers=(
                    AnswerData(label=letter, text=sample[f"answer_option{i}"])
                    for i, letter in enumerate(letters[:answer_num])
                ),
            )
