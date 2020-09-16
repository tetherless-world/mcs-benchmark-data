from typing import NamedTuple

class BenchmarkChoice(NamedTuple):
    #A possible choice for a benchmark sample
    #Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution
    id: str
    text: str
    position: int #necessary?