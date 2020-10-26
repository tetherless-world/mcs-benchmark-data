import logging
import json
import xmltodict
from abc import abstractmethod
from pathlib import Path
from rdflib import URIRef
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer

from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_bootstrap import BenchmarkBootstrap
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset


class _Benchmark_Transformer(_Transformer):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    @property
    def _uri_base(self):
        return f"benchmark:{self._pipeline_id}"

    @property
    def _benchmark_dataset_classes(self):
        return {
            "dev": BenchmarkDevDataset,
            "test": BenchmarkTestDataset,
            "train": BenchmarkTrainDataset,
        }

    def _transform(self, **kwds) -> Generator[_Model, None, None]:

        benchmark_json_file_path = kwds["extracted_path"] / getattr(
            kwds["file_names"], "meta_data"
        )

        with open(benchmark_json_file_path) as benchmark_json:
            benchmark_metadata = json.loads(benchmark_json.read())

        benchmark_bootstrap = BenchmarkBootstrap.from_dict(benchmark_metadata)

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

            new_dataset = self._benchmark_dataset_classes[dataset_type](
                uri=dataset_uri, benchmark_uri=benchmark.uri, name=dataset["name"]
            )

            yield new_dataset

            yield from self._transform_benchmark_sample(
                dataset_type=dataset_type,
                dataset_uri=new_dataset.uri,
                **kwds,
            )

    def _prepare_sample(
        self,
        *,
        dataset_type: str,
        dataset_uri: URIRef,
        sample: dict,
        correct_choice: int,
        **kwds,
    ) -> Generator[_Model, None, None]:

        correct_choice = None

        if dataset_type != "test":
            correct_choice = URIRef(
                f"{dataset_uri}:sample:{sample['id']}:hypothesis:{correct_choice}"
            )

        benchmark_sample = BenchmarkSample(
            uri=URIRef(f"{dataset_uri}:sample:{sample['id']}"),
            dataset_uri=dataset_uri,
            correct_choice=correct_choice,
        )

        yield benchmark_sample

        yield BenchmarkQuestionType.multiple_choice(
            uri_base=self._uri_base,
            benchmark_sample_uri=benchmark_sample.uri,
        )

    @abstractmethod
    def _transform_benchmark_sample(
        self, *, dataset_type: str, dataset_uri: URIRef, **kwds
    ) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
