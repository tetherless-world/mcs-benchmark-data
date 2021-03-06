import json
from abc import abstractmethod
from pathlib import Path
from rdflib import URIRef
from typing import Generator, Optional, Tuple, List, Dict

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer

from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_metadata import BenchmarkMetadata
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_goal import BenchmarkGoal
from mcs_benchmark_data.models.benchmark_solution import BenchmarkSolution
from mcs_benchmark_data.models.benchmark_observation import BenchmarkObservation
from mcs_benchmark_data.models.benchmark_hypothesis import BenchmarkHypothesis
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.dataset_content_type import DatasetContentType


class _BenchmarkTransformer(_Transformer):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    @property
    def __benchmark_dataset_classes(self):
        return {
            "dev": BenchmarkDevDataset,
            "test": BenchmarkTestDataset,
            "train": BenchmarkTrainDataset,
        }

    @property
    def _uri_base(self):
        return URIRef(f"benchmark:{self._pipeline_id}")

    def _benchmark_sample_uri(self, *, dataset_uri: URIRef, sample_id: str):
        return URIRef(f"{dataset_uri}:sample:{sample_id}")

    def _sample_labels_lst_file_path(self, *, dataset_type: DatasetType):
        return (
            self._pipeline_data_dir_path
            / "datasets"
            / dataset_type.value
            / f"{dataset_type.value}_labels.lst"
        )

    def _sample_jsonl_file_path(
        self, *, dataset_type: DatasetType, dataset_content_type: DatasetContentType
    ):
        """
        returns file path of the type of file indicated by the parameters
        @param dataset_type the type of dataset (i.e. dev, test, train)
        @param content_type the type of information contained in the file (i.e. samples, labels)

        """
        return (
            self._pipeline_data_dir_path
            / "datasets"
            / dataset_type.value
            / f"{dataset_type.value}_{dataset_content_type.value}.jsonl"
        )

    def _sample_xml_file_path(self, *, dataset_type: DatasetType):
        return (
            self._pipeline_data_dir_path
            / "datasets"
            / dataset_type.value
            / f"{dataset_type.value}_samples.xml"
        )

    def _generate_none(self) -> Generator[None, None, None]:
        while True:
            yield None

    def _read_jsonl_file(
        self,
        jsonl_file_path: Path,
    ) -> Generator[Dict[str, object], None, None]:
        with open(jsonl_file_path) as jsonl_file:
            for line in jsonl_file:
                if not line.strip():
                    continue
                yield json.loads(line)

    def transform(self, **kwds) -> Generator[_Model, None, None]:

        benchmark_json_file_path = self._pipeline_data_dir_path / "metadata.json"

        with open(benchmark_json_file_path) as benchmark_json:
            benchmark_metadata = json.loads(benchmark_json.read())

        benchmark_bootstrap = BenchmarkMetadata.from_dict(benchmark_metadata)

        benchmark = Benchmark(
            uri=self._uri_base,
            name=benchmark_bootstrap.name,
            abstract=benchmark_bootstrap.abstract,
            authors=tuple(author["name"] for author in benchmark_bootstrap.authors),
        )

        yield benchmark

        for dataset in benchmark_metadata["datasets"]:

            dataset_type = getattr(DatasetType, dataset["@id"].split("/")[-1].upper())

            dataset_uri = URIRef(f"{self._uri_base}:dataset:{dataset['@id']}")

            new_dataset = self.__benchmark_dataset_classes[dataset_type.value](
                uri=dataset_uri, benchmark_uri=benchmark.uri, name=dataset["name"]
            )

            yield new_dataset

            yield from self._transform_benchmark_sample(
                dataset_type=dataset_type,
                dataset_uri=new_dataset.uri,
                **kwds,
            )

    def _yield_sample_concept_context(
        self,
        *,
        dataset_uri: URIRef,
        sample_id: str,
        correct_choice: URIRef,
        concepts: Optional[Tuple[str, ...]],
        context: Optional[str],
        **kwds,
    ):
        benchmark_sample = BenchmarkSample(
            uri=self._benchmark_sample_uri(
                dataset_uri=dataset_uri, sample_id=sample_id
            ),
            dataset_uri=dataset_uri,
            correct_choice=correct_choice,
        )

        yield benchmark_sample

        if concepts is not None:
            for i, concept in enumerate(concepts):
                yield BenchmarkConcept(
                    uri=URIRef(f"{benchmark_sample.uri}:concept:{i}"),
                    benchmark_sample_uri=benchmark_sample.uri,
                    concept=concept,
                )

        if context is not None:
            yield BenchmarkContext(
                uri=URIRef(f"{benchmark_sample.uri}:context"),
                benchmark_sample_uri=benchmark_sample.uri,
                text=context,
            )

    def _yield_qa_models(
        self,
        *,
        dataset_uri: URIRef,
        benchmark_sample_uri: str,
        question: str,
        answers: Tuple[AnswerData, ...],
        **kwds,
    ) -> Generator[_Model, None, None]:

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        yield BenchmarkQuestion(
            uri=URIRef(f"{benchmark_sample_uri}:question"),
            benchmark_sample_uri=benchmark_sample_uri,
            text=question,
        )

        for answer in answers:
            label = getattr(answer, "label")
            text = getattr(answer, "text")
            yield BenchmarkAnswer(
                uri=URIRef(f"{benchmark_sample_uri}:answer:{label}"),
                benchmark_sample_uri=benchmark_sample_uri,
                position=ans_mapping[label],
                text=text,
            )

    def _yield_goal_models(
        self,
        *,
        dataset_uri: URIRef,
        sample_id: str,
        benchmark_sample_uri: URIRef,
        goal: str,
        solutions: Tuple[str, str],
        **kwds,
    ) -> Generator[_Model, None, None]:

        yield BenchmarkGoal(
            uri=URIRef(f"{benchmark_sample_uri}:goal"),
            benchmark_sample_uri=benchmark_sample_uri,
            text=goal,
        )

        for i, solution in enumerate(solutions):
            yield BenchmarkSolution(
                uri=URIRef(f"{benchmark_sample_uri}:solution:{i+1}"),
                benchmark_sample_uri=benchmark_sample_uri,
                position=i + 1,
                text=solution,
            )

    def _yield_observation_models(
        self,
        *,
        dataset_uri: URIRef,
        sample_id: str,
        benchmark_sample_uri: URIRef,
        observations: Tuple[str, str],
        hypotheses: Tuple[str, str],
        **kwds,
    ) -> Generator[_Model, None, None]:

        for i, observation in enumerate(observations):
            yield BenchmarkObservation(
                uri=URIRef(f"{benchmark_sample_uri}:observation:{i+1}"),
                benchmark_sample_uri=benchmark_sample_uri,
                text=observation,
            )

        for i, hypothesis in enumerate(hypotheses):
            yield BenchmarkHypothesis(
                uri=URIRef(f"{benchmark_sample_uri}:hypothesis:{i+1}"),
                benchmark_sample_uri=benchmark_sample_uri,
                position=i + 1,
                text=hypothesis,
            )

    @abstractmethod
    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models
        :return: generator of models
        """
