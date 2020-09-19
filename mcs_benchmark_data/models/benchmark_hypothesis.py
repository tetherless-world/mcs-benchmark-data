from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkHypothesis(BenchmarkChoice):
    '''A benchmark's sample hypothesis choice'''
    '''Choice of observations (aNLI)'''
