from typing import Tuple

from mcs_benchmark_data.models.model import Model

class BenchmarkConcept(Model):
    '''The ConceptNet concept which the question was created from (i.e. electricity)'''
    concept: Tuple[str, ...]