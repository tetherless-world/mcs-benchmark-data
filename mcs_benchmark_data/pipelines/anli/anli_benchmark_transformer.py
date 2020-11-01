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
from mcs_benchmark_data.pipelines.anli.anli_benchmark_file_names import (
    AnliBenchmarkFileNames,
)
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class AnliBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        extracted_data_dir_path: Path,
        file_names: AnliBenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = (
                extracted_data_dir_path
                / "dataset"
                / getattr(file_names, dataset_type + "_labels")
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = (
            extracted_data_dir_path
            / "dataset"
            / getattr(file_names, dataset_type + "_samples")
        )

        with open(sample_jsonl_file_path) as all_samples:

            for i, line in enumerate(all_samples):

                if line == "\n":
                    continue

                sample = json.loads(line)

                sample_id = f"{sample['story_id']}"

                benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample_id}")

                correct_choice = None

                if dataset_type != "test":
                    correct_choice = URIRef(
                        f"{dataset_uri}:sample:{sample_id}:correct_choice:{all_labels[i]}"
                    )

                yield BenchmarkQuestionType.multiple_choice(
                    uri_base=self._uri_base,
                    benchmark_sample_uri=URIRef(benchmark_sample_uri),
                )

                yield from self._yield_sample_concept_context(
                    dataset_uri=dataset_uri,
                    sample_id=sample_id,
                    concepts=None,
                    context=None,
                    correct_choice=correct_choice,
                )

                yield from self._yield_obs_models(
                    dataset_uri=dataset_uri,
                    sample_id=sample_id,
                    benchmark_sample_uri=benchmark_sample_uri,
                    observations=tuple((sample["obs1"], sample["obs2"])),
                    hypotheses=tuple((sample["hyp1"], sample["hyp2"])),
                )
