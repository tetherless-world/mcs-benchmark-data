import json
import itertools
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.dataset_content_type import DatasetContentType


class CycicBenchmarkTransformer(_BenchmarkTransformer):
    ANSWER_CHOICES = tuple(("A", "B", "C", "D", "E"))

    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = self._sample_jsonl_file_path(
                dataset_type=dataset_type,
                dataset_content_type=DatasetContentType.LABELS,
            )

            all_labels = self._read_jsonl_file(sample_labels_file_path)
        else:
            all_labels = self._generate_none()

        sample_jsonl_file_path = self._sample_jsonl_file_path(
            dataset_type=dataset_type,
            dataset_content_type=DatasetContentType.SAMPLES,
        )

        for sample, label_entry in zip(
            self._read_jsonl_file(sample_jsonl_file_path), all_labels
        ):

            sample_id = f"{sample['run_id']}_{sample['guid']}"

            benchmark_sample_uri = self._benchmark_sample_uri(
                dataset_uri=dataset_uri, sample_id=sample_id
            )

            yield BenchmarkQuestionType.multiple_choice(
                uri_base=self._uri_base,
                benchmark_sample_uri=benchmark_sample_uri,
            )

            answer_num = 0

            while f"answer_option{answer_num}" in sample:
                answer_num += 1

            yield from self._yield_sample_concept_context(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                concepts=tuple(sample["categories"]),
                context=None,
                correct_choice=URIRef(
                    f"{dataset_uri}:sample:{sample_id}:correct_choice:{label_entry['correct_answer']}"
                )
                if label_entry is not None
                else None,
            )

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                benchmark_sample_uri=benchmark_sample_uri,
                question=sample["question"],
                answers=tuple(
                    AnswerData(label=answer_choice, text=sample[f"answer_option{i}"])
                    for i, answer_choice in enumerate(self.ANSWER_CHOICES[:answer_num])
                ),
            )
