from mcs_benchmark_data.models.model import Model
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_question_category import BenchmarkQuestionCategory


class BenchmarkSample(Model):
    '''An entry in a benchmark dataset'''
    name: str
    text: str
    context: BenchmarkContext
    question_type: BenchmarkQuestionType
    question_category: BenchmarkQuestionCategory