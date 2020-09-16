from typing import NamedTuple, Tuple
from datetime import datetime

from mcs-benchmark-data.dev_score import DevScore
from mcs-benchmark-data.test_score import TestScore

class Submission(NamedTuple):
    #A submission dataset from a system/model with prediction choices for a benchmark.
    id: str
    name: str
    description: str
    dateCreated: datetime
    isBasedOn: str #benchmark name
    contributor: Tuple[str, ...]
    contentRating: Tuple[TestScore, DevScore]
