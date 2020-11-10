import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class CommonsenseQaBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_jsonl_file_path = (
            self._data_dir_path
            / "datasets"
            / dataset_type
            / f"{dataset_type}_samples.jsonl"
        )

        for sample in self._read_jsonl_file(sample_jsonl_file_path):

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
