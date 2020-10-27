import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef
from dataclasses_json import dataclass_json

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.pipelines.cycic.cycic_benchmark_file_names import (
    CycicBenchmarkFileNames,
)
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class CycicBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        extracted_data_dir_path: Path,
        file_names: CycicBenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = extracted_data_dir_path / getattr(
                file_names, dataset_type + "_labels"
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = extracted_data_dir_path / getattr(
            file_names, dataset_type + "_samples"
        )

        with open(sample_jsonl_file_path) as all_samples:

            for i, sample in enumerate(all_samples):

                sample = json.loads(sample)

                label_entry = json.loads(all_labels[i])

                sample_id = f"{sample['run_id']}_{sample['guid']}"

                benchmark_sample_uri_str = f"{dataset_uri}:sample:{sample_id}"

                correct_choice = None

                if dataset_type != "test":
                    correct_choice = URIRef(
                        f"{dataset_uri}:sample:{sample_id}:correct_choice:{label_entry['correct_answer']}"
                    )

                yield BenchmarkQuestionType.multiple_choice(
                    uri_base=self._uri_base,
                    benchmark_sample_uri=URIRef(benchmark_sample_uri_str),
                )

                letters = ["A", "B", "C", "D", "E"]

                answer_num = 0

                while f"answer_option{i}" in sample:
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
