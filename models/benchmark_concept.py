from typing import NamedTuple, Tuple


class BenchmarkConcept(NamedTuple):
    #The ConceptNet concept which the question was created from (i.e. electricity)
    concept: Tuple[str, ...]