from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkQuestion(BenchmarkPrompt):
    '''A benchmark's sample question element'''