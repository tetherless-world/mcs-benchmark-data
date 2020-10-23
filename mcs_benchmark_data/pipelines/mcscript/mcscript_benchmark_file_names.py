from typing import NamedTuple
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class MCScriptBenchmarkFileNames(_BenchmarkFileNames):
    dev_samples: str = "dev-data.xml"
    train_samples: str = "train-data.xml"
    test_samples: str = "test-data.xml"
