from typing import NamedTuple

class DevScore(NamedTuple):
    #Score of a system's correct predictions against a dev benchmark dataset
    name: str
    value: str