import logging
import json
from abc import abstractmethod
from pathlib import Path
from rdflib import URIRef
from typing import Generator, Optional, Tuple

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer

from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_metadata import BenchmarkMetadata
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_goal import BenchmarkGoal
from mcs_benchmark_data.models.benchmark_hypothesis import BenchmarkHypothesis
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer


class _BenchmarkTransformer(_Transformer):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    @property
    def _uri_base(self):
        return f"benchmark:{self._pipeline_id}"

    @property
    def __benchmark_dataset_classes(self):
        return {
            "dev": BenchmarkDevDataset,
            "test": BenchmarkTestDataset,
            "train": BenchmarkTrainDataset,
        }

    def _transform(
        self, *, extracted_path: Path, file_names: _BenchmarkFileNames, **kwds
    ) -> Generator[_Model, None, None]:

        benchmark_json_file_path = extracted_path / getattr(file_names, "metadata")

        with open(benchmark_json_file_path) as benchmark_json:
            benchmark_metadata = json.loads(benchmark_json.read())

        benchmark_bootstrap = BenchmarkMetadata.from_dict(benchmark_metadata)

        benchmark = Benchmark(
            uri=URIRef(f"{self._uri_base}:benchmark:{benchmark_metadata['@id']}"),
            name=benchmark_bootstrap.name,
            abstract=benchmark_bootstrap.abstract,
            authors=tuple(author["name"] for author in benchmark_bootstrap.authors),
        )

        yield benchmark

        for dataset in benchmark_metadata["datasets"]:

            dataset_type = dataset["@id"].split("/")[-1]

            dataset_uri = URIRef(f"{self._uri_base}:dataset:{dataset['@id']}")

            new_dataset = self.__benchmark_dataset_classes[dataset_type](
                uri=dataset_uri, benchmark_uri=benchmark.uri, name=dataset["name"]
            )

            yield new_dataset

            yield from self._transform_benchmark_sample(
                extracted_path=extracted_path,
                file_names=file_names,
                dataset_type=dataset_type,
                dataset_uri=new_dataset.uri,
                **kwds,
            )

    def _yield_qa_models(
        self,
        *,
        dataset_uri: URIRef,
        sample_id: str,
        concepts: Optional[Tuple[str, ...]],
        context: Optional[str],
        correct_choice: URIRef,
        question: str,
        answers: Tuple[Tuple[str, str], ...],
        **kwds,
    ) -> Generator[_Model, None, None]:

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        benchmark_sample = BenchmarkSample(
            uri=URIRef(f"{dataset_uri}:sample:{sample_id}"),
            dataset_uri=dataset_uri,
            correct_choice=correct_choice,
        )

        yield benchmark_sample

        yield BenchmarkQuestionType.multiple_choice(
            uri_base=self._uri_base,
            benchmark_sample_uri=benchmark_sample.uri,
        )

        if concepts is not None:
            for i in range(len(concepts)):
                yield BenchmarkConcept(
                    uri=URIRef(f"{benchmark_sample.uri}:concept:{i}"),
                    benchmark_sample_uri=benchmark_sample.uri,
                    concept=concepts[i],
                )

        if context is not None:
            yield BenchmarkContext(
                uri=URIRef(f"{benchmark_sample.uri}:context"),
                benchmark_sample_uri=benchmark_sample.uri,
                text=context,
            )

        yield BenchmarkQuestion(
            uri=URIRef(f"{benchmark_sample.uri}:question"),
            benchmark_sample_uri=benchmark_sample.uri,
            text=question,
        )

        for answer in answers:
            yield BenchmarkAnswer(
                uri=URIRef(f"{benchmark_sample.uri}:answer:{answer[1]}"),
                benchmark_sample_uri=benchmark_sample.uri,
                position=ans_mapping[answer[1]],
                text=answer[0],
            )

    def _yield_goal_models(
        self,
        *,
        dataset_uri: URIRef,
        sample_id: str,
        concepts: Optional[Tuple[str, ...]],
        context: Optional[str],
        correct_choice: URIRef,
        goal: str,
        hypotheses: Tuple[str, ...],
        **kwds,
    ) -> Generator[_Model, None, None]:

        benchmark_sample = BenchmarkSample(
            uri=URIRef(f"{dataset_uri}:sample:{sample_id}"),
            dataset_uri=dataset_uri,
            correct_choice=correct_choice,
        )

        yield benchmark_sample

        yield BenchmarkQuestionType.multiple_choice(
            uri_base=self._uri_base,
            benchmark_sample_uri=benchmark_sample.uri,
        )

        if concepts is not None:
            for i in range(len(concepts)):
                yield BenchmarkConcept(
                    uri=URIRef(f"{benchmark_sample.uri}:concept"),
                    benchmark_sample_uri=benchmark_sample.uri,
                    concept=concepts[i],
                )

        if context is not None:
            yield BenchmarkContext(
                uri=URIRef(f"{benchmark_sample.uri}:context"),
                benchmark_sample_uri=benchmark_sample.uri,
                text=context,
            )

        yield BenchmarkQuestionType.multiple_choice(
            uri_base=self._uri_base,
            benchmark_sample_uri=benchmark_sample.uri,
        )

        yield BenchmarkGoal(
            uri=URIRef(f"{benchmark_sample.uri}:goal"),
            benchmark_sample_uri=benchmark_sample.uri,
            text=goal,
        )

        for i in range(len(hypotheses)):
            yield BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample.uri}:hypothesis:{i+1}"),
                benchmark_sample_uri=benchmark_sample.uri,
                position=i + 1,
                text=hypotheses[i],
            )

    @abstractmethod
    def _transform_benchmark_sample(
        self,
        *,
        extracted_path: Path,
        file_names: _BenchmarkFileNames,
        dataset_type: str,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
