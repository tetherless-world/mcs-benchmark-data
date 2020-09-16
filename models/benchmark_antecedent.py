from typing import Tuple, Union

from mcs-benchmark-data.model.benchmark_question import BenchmarkQuestion
from mcs-benchmark-data.model.benchmark_context import BenchmarkContext


class BenchmarkAntecedent(NamedTuple):
    #A list of elements that compose a benchmark sample
    id: str
    numberOfElements: int
    elements: Union[Tuple[BenchmarkContext, BenchmarkQuestion], Tuple[BenchmarkQuestion]]
