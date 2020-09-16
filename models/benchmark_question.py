from typing import NamedTuple


class BenchmarkQuestion(NamedTuple):
    #A benchmark's sample question element
    id: str
    name: str
    text: str
    position: int #necessary?