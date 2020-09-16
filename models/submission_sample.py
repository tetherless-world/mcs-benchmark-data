from typing import NamedTuple, Tuple

class Submission(NamedTuple):
    #A submission dataset from a system/model with prediction choices for a benchmark.
    id: str
    type: str
    includedInDataset: str
    value: int
    about: str