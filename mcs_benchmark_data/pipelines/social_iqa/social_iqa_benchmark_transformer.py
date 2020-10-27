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
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_file_names import (
    SocialIQaBenchmarkFileNames,
)


class SocialIQaBenchmarkTransformer(_BenchmarkTransformer):
    def transform(
        self,
        *,
        extracted_path: Path,
        file_names: SocialIQaBenchmarkFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:
        yield from _BenchmarkTransformer._transform(
            self, extracted_path=extracted_path, file_names=file_names, **kwds
        )

    def _transform_benchmark_sample(
        self,
        *,
        extracted_path: Path,
        file_names: SocialIQaBenchmarkFileNames,
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

        i = 0

        for line in all_samples:

            sample = json.loads(line)

            correct_choice = None

            if dataset_type != "test":
                correct_choice = URIRef(
                    f"{dataset_uri}:sample:{i}:correct_choice:{int(all_labels[i]) + 1}"
                )

            question = sample["question"]

            context = sample["context"]

            answers = []

            for letter in ["A", "B", "C"]:
                answer = ("answer{letter}", letter)
                answers.append(answer)

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=i,
                concepts=None,
                context=context,
                correct_choice=correct_choice,
                question=question,
                answers=answers,
            )

            i += 1
