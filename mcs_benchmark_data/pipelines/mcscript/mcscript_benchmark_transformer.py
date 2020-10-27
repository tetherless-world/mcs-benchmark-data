import json
import os
import xmltodict
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
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_file_names import (
    MCScriptBenchmarkFileNames,
)


class MCScriptBenchmarkTransformer(_BenchmarkTransformer):
    def transform(
        self, *, extracted_path: Path, file_names: MCScriptBenchmarkFileNames, **kwds
    ) -> Generator[_Model, None, None]:

        yield from _BenchmarkTransformer._transform(
            self, extracted_path=extracted_path, file_names=file_names, **kwds
        )

    def _transform_benchmark_sample(
        self,
        *,
        extracted_path: Path,
        file_names: MCScriptBenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        sample_xml_file_path = extracted_path / getattr(
            file_names, dataset_type + "_samples"
        )
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

                benchmark_sample_uri = URIRef(
                    f"{dataset_uri}:sample:{sample['@id']}_{question['@id']}"
                )

                yield BenchmarkConcept(
                    uri=URIRef(f"{benchmark_sample_uri}:concept"),
                    benchmark_sample_uri=benchmark_sample_uri,
                    concept=sample["@scenario"],
                )

                yield BenchmarkContext(
                    uri=URIRef(f"{benchmark_sample_uri}:context"),
                    benchmark_sample_uri=benchmark_sample_uri,
                    text=sample["text"],
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

                for answer in question["answer"]:
                    benchmark_answer = BenchmarkAnswer(
                        uri=URIRef(
                            f"{benchmark_question.uri}:choice:{str(answer['@id'])}"
                        ),
                        benchmark_sample_uri=benchmark_sample_uri,
                        position=answer["@id"],
                        text=answer["@text"],
                    )

                    yield benchmark_answer

                    if dataset_type != "test" and answer["@correct"] == "True":
                        correct_choice = URIRef(
                            f"{benchmark_question.uri}:correct_choice:{answer['@id']}"
                        )

                yield BenchmarkSample(
                    uri=benchmark_sample_uri,
                    dataset_uri=dataset_uri,
                    correct_choice=correct_choice,
                )
