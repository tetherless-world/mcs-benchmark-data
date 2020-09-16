from typing import NamedTuple, Tuple

from mcs-benchmark-data.model.benchmark_answer import BenchmarkAnswer


class BenchmarkChoices(NamedTuple):
    #List of possible choices in a benchmark sample
    id: str
    numberOfItems: int
    choices: Tuple[BenchmarkChoice, ...]