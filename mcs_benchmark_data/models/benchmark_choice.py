from mcs_benchmark_data.models.model import Model

class BenchmarkChoice(Model):
    '''A possible choice for a benchmark sample'''
    '''Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution'''
    text: str
    position: int #necessary?