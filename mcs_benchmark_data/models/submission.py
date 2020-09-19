from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from datetime import datetime
from typing import Tuple

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.dev_score import DevScore
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.submission_sample import SubmissionSample

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class Submission(_Model):
    '''A submission dataset from a system/model with prediction choices for a benchmark'''
    name: str
    description: str
    dateCreated: datetime
    isBasedOn: str #benchmark name
    contributor: Tuple[str, ...]
    contentRating: Tuple[TestScore, DevScore]
    result: Tuple[str, datetime, datetime, str] #type (e.g. SoftwareAplication), startTime, endTime, url
    sample: Tuple[SubmissionSample, ...]