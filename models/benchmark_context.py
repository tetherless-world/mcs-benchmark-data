from typing import NamedTuple


class BenchmarkContext(NamedTuple):
    #Context element of a benchmark sample
    name: str
    text: str
    position: int #necessary