from mcs_benchmark_data.models.model import Model

class BenchmarkContext(Model):
    '''Context element of a benchmark sample'''
    name: str
    text: str
    position: int #necessary