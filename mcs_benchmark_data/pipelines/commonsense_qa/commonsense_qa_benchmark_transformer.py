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
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_file_names import (
    CommonsenseQaBenchmarkFileNames,
)


class CommonsenseQaBenchmarkTransformer(_BenchmarkTransformer):
    def transform(
        self,
        *,
        extracted_path: Path,
        file_names: CommonsenseQaBenchmarkFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:
        yield from _BenchmarkTransformer._transform(
            self, extracted_path=extracted_path, file_names=file_names, **kwds
        )

    def _transform_benchmark_sample(
        self,
        *,
        extracted_path: Path,
        file_names: CommonsenseQaBenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_jsonl_file_path = extracted_path / getattr(
            file_names, dataset_type + "_samples"
        )

        with open(sample_jsonl_file_path) as file:

            all_samples = list(file)

        for line in all_samples:

            sample = json.loads(line)

            correct_choice = None

            if dataset_type != "test":
                correct_choice = URIRef(
                    f"{dataset_uri}:sample:{sample['id']}:correct_choice:{sample['answerKey']}"
                )

            concept = [sample["question"]["question_concept"]]

            question = sample["question"]["stem"]

            answers = []

            for item in sample["question"]["choices"]:
                answer_tuple = (item["text"], item["label"])
                answers.append(answer_tuple)

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=sample["id"],
                concepts=concept,
                context=None,
                correct_choice=correct_choice,
                question=question,
                answers=answers,
            )
