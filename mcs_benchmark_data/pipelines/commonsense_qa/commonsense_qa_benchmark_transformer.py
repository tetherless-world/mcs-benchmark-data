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
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample


class CommonsenseQaBenchmarkTransformer(_Benchmark_Transformer):
    def transform(self, **kwds) -> Generator[_Model, None, None]:
        yield from _Benchmark_Transformer._transform(self, **kwds)

    def _transform_benchmark_sample(
        self, dataset_type: str, dataset_uri: URIRef, **kwds
    ) -> Generator[_Model, None, None]:

        sample_jsonl_file_path = kwds["extracted_path"] / getattr(
            kwds["file_names"], dataset_type + "_samples"
        )

        with open(sample_jsonl_file_path) as file:

            all_samples = list(file)

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        for line in all_samples:

            sample = json.loads(line)

            benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{sample['id']}")

            correct_choice = None

            if dataset_type != "test":
                correct_choice = sample["answerKey"]

            yield from _Benchmark_Transformer._prepare_sample(
                self,
                dataset_type=dataset_type,
                dataset_uri=dataset_uri,
                sample=sample,
                correct_choice=correct_choice,
            )

            yield BenchmarkConcept(
                uri=URIRef(f"{benchmark_sample_uri}:concept"),
                benchmark_sample_uri=benchmark_sample_uri,
                concept=sample["question"]["question_concept"],
            )

            yield BenchmarkQuestion(
                uri=URIRef(f"{benchmark_sample_uri}:question"),
                benchmark_sample_uri=benchmark_sample_uri,
                text=sample["question"]["stem"],
            )

            for item in sample["question"]["choices"]:
                yield BenchmarkAnswer(
                    uri=URIRef(f"{benchmark_sample_uri}:choice:{item['label']}"),
                    benchmark_sample_uri=benchmark_sample_uri,
                    position=ans_mapping[item["label"]],
                    text=item["text"],
                )
