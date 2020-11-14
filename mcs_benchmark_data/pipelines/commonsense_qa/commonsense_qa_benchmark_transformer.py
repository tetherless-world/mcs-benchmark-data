import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.dataset_content_type import DatasetContentType


class CommonsenseQaBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_jsonl_file_path = self._sample_jsonl_file_path(
            dataset_type=dataset_type,
            dataset_content_type=DatasetContentType.SAMPLES,
        )

        for sample in self._read_jsonl_file(sample_jsonl_file_path):

            sample_id = sample["id"]

            benchmark_sample_uri = self._benchmark_sample_uri(
                dataset_uri=dataset_uri, sample_id=sample_id
            )

            yield BenchmarkQuestionType.multiple_choice(
                uri_base=self._uri_base,
                benchmark_sample_uri=benchmark_sample_uri,
            )

            yield from self._yield_sample_concept_context(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                concepts=tuple([sample["question"]["question_concept"]]),
                context=None,
                correct_choice=URIRef(
                    f"{benchmark_sample_uri}:correct_choice:{sample['answerKey']}"
                )
                if dataset_type != DatasetType.TEST
                else None,
            )

            yield from self._yield_qa_models(
                dataset_uri=dataset_uri,
                sample_id=sample_id,
                benchmark_sample_uri=benchmark_sample_uri,
                question=sample["question"]["stem"],
                answers=tuple(
                    AnswerData(label=item["label"], text=item["text"])
                    for item in sample["question"]["choices"]
                ),
            )
