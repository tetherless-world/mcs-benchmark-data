from typing import Tuple, Union

from mcs_benchmark_data.models.model import Model
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext


class BenchmarkAntecedent(Model):
    '''A list of elements that compose a benchmark sample'''
    numberOfElements: int
    elements: Union[Tuple[BenchmarkContext, BenchmarkQuestion], Tuple[BenchmarkQuestion]]
