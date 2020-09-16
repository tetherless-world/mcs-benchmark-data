from typing import NamedTuple

from mcs-benchmark-data.benchmark_context import BenchmarkContext
from mcs-benchmark-data.benchmark_question_type import BenchmarkQuestionType
from mcs-benchmark-data.benchmark_question_category import BenchmarkQuestionCategory


class BenchmarkSample(NamedTuple):
    #An entry in a benchmark dataset
    id: str
    name: str
    text: str
    context: BenchmarkContext
    question_type: BenchmarkQuestionType