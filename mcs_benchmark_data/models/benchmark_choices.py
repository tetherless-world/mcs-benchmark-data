from typing import Tuple

from mcs_benchmark_data.models.model import Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


class BenchmarkChoices(Model):
    '''List of possible choices in a benchmark sample'''
    numberOfItems: int
    choices: Tuple[BenchmarkChoice, ...]