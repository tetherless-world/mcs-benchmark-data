from mcs_benchmark_data.dataset_type import DatasetType
from rdflib import URIRef
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer


class BenchmarkNameBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:
        """
        TODO: - Read and iterate through the samples from the given dataset
              - Yield each sample and the models associated with the benchmark
              - Consult the helper functions in _BenchmarkTransformer for guidance
        """
