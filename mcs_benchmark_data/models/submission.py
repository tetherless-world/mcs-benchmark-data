from datetime import datetime

from mcs_benchmark_data.models.model import Model
from mcs_benchmark_data.models.dev_score import DevScore
from mcs_benchmark_data.models.test_score import TestScore

class Submission(Model):
    '''A submission dataset from a system/model with prediction choices for a benchmark'''
    name: str
    description: str
    dateCreated: datetime
    isBasedOn: str #benchmark name
    contributor: Tuple[str, ...]
    contentRating: Tuple[TestScore, DevScore]
    result: #Are we missing a result object here?? 
