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


class CycicBenchmarkTransformer(_BenchmarkTransformer):
    def transform(
        self,
        *,
        extracted_path: Path,
        file_names: CycicBenchmarkFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:
        yield from _BenchmarkTransformer._transform(
            self, extracted_path=extracted_path, file_names=file_names, **kwds
        )

    def _transform_benchmark_sample(
        self,
        *,
        extracted_path: Path,
        file_names: CycicBenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        if dataset_type != "test":
            sample_labels_file_path = extracted_path / getattr(
                file_names, dataset_type + "_labels"
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = extracted_path / getattr(
            file_names, dataset_type + "_samples"
        )

        with open(sample_jsonl_file_path) as sample_file:
            all_samples = list(sample_file)

        for i in range(len(all_samples)):

            sample = json.loads(all_samples[i])

            label_entry = json.loads(all_labels[i])

            sample_id = f"{sample['run_id']}_{sample['guid']}"

            correct_choice = None

            if dataset_type != "test":
                correct_choice = URIRef(
                    f"{dataset_uri}:sample:{sample_id}:correct_choice:{label_entry['correct_answer']}"
                )

            question = sample["question"]

            concepts = sample["categories"]

            answers = []

            letters = ["A", "B", "C", "D", "E"]

            for i in range(len(letters)):
                answer = ("answer_option{i}", letters[i])
                answers.append(answer)

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                concepts=concepts,
                context=None,
                correct_choice=correct_choice,
                question=question,
                answers=answers,
            )
