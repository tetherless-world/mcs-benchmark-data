from typing import NamedTuple, Tuple

class Submission(NamedTuple):
    #An entry in a submission dataset (i.e. prediction)
    id: str
    type: str
    includedInDataset: str
    value: int
    about: str