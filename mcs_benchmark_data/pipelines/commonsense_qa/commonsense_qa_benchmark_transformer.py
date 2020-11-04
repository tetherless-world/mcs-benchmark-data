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
from mcs_benchmark_data.inline_labels_benchmark_file_names import (
    InlineLabelsBenchmarkFileNames,
)
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class CommonsenseQaBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        extracted_data_dir_path: Path,
        file_names: InlineLabelsBenchmarkFileNames,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_jsonl_file_path = (
            extracted_data_dir_path
            / "datasets"
            / getattr(file_names, dataset_type + "_samples")
        )

        with open(sample_jsonl_file_path) as all_samples:

            for line in all_samples:
                if not line.strip():
                    continue

                sample = json.loads(line)

                sample_id = sample["id"]

                benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample_id}")

                correct_choice = None

                if dataset_type != DatasetType.TEST.value:
                    correct_choice = URIRef(
                        f"{benchmark_sample_uri}:correct_choice:{sample['answerKey']}"
                    )

                yield BenchmarkQuestionType.multiple_choice(
                    uri_base=self._uri_base,
                    benchmark_sample_uri=URIRef(benchmark_sample_uri),
                )

                yield from self._yield_sample_concept_context(
                    dataset_uri=dataset_uri,
                    sample_id=sample_id,
                    concepts=[sample["question"]["question_concept"]],
                    context=None,
                    correct_choice=correct_choice,
                )

                yield from self._yield_qa_models(
                    dataset_uri=dataset_uri,
                    sample_id=sample_id,
                    benchmark_sample_uri=benchmark_sample_uri,
                    question=sample["question"]["stem"],
                    answers=(
                        AnswerData(label=item["label"], text=item["text"])
                        for item in sample["question"]["choices"]
                    ),
                )
