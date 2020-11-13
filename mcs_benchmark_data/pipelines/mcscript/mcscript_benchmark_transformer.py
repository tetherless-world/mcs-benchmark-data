import xmltodict
import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType


class MCScriptBenchmarkTransformer(_BenchmarkTransformer):
    ANSWER_CHOICES = tuple(("A", "B"))

    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_xml_file_path = self._sample_xml_file_path(dataset_type=dataset_type)

        with open(sample_xml_file_path) as sample_file:
            all_samples = xmltodict.parse(sample_file.read())

        sample_dict = all_samples["data"]["instance"]

        for sample in sample_dict:

            correct_choice = None

            if not sample["questions"]:
                continue

            for question in sample["questions"]["question"]:

                if not isinstance(question, dict):
                    continue

                sample_id = URIRef(f"{sample['@id']}_{question['@id']}")

                benchmark_sample_uri = self._benchmark_sample_uri(
                    dataset_uri=dataset_uri, sample_id=sample_id
                )

                yield BenchmarkQuestionType.multiple_choice(
                    uri_base=self._uri_base,
                    benchmark_sample_uri=benchmark_sample_uri,
                )

                benchmark_question = BenchmarkQuestion(
                    uri=URIRef(f"{benchmark_sample_uri}:question:{question['@id']}"),
                    benchmark_sample_uri=benchmark_sample_uri,
                    text=question["@text"],
                )

                yield benchmark_question

                yield from self._yield_qa_models(
                    dataset_uri=dataset_uri,
                    sample_id=sample_id,
                    benchmark_sample_uri=benchmark_sample_uri,
                    question=question["@text"],
                    answers=tuple(
                        AnswerData(
                            label=self.ANSWER_CHOICES[int(answer["@id"])],
                            text=answer["@text"],
                        )
                        for answer in question["answer"]
                    ),
                )

                if dataset_type.value != DatasetType.TEST.value:
                    for answer in question["answer"]:
                        if answer["@correct"] == "True":
                            correct_choice = URIRef(
                                f"{benchmark_question.uri}:correct_choice:{answer['@id']}"
                            )
                            break

                yield from self._yield_sample_concept_context(
                    dataset_uri=dataset_uri,
                    sample_id=URIRef(f"{sample['@id']}_{question['@id']}"),
                    concepts=tuple([sample["@scenario"]]),
                    context=sample["text"],
                    correct_choice=correct_choice,
                )
