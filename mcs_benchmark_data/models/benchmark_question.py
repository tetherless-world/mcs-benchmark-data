from mcs_benchmark_data.models.model import Model


class BenchmarkQuestion(Model):
    '''A benchmark's sample question element'''
    name: str
    text: str
    position: int #necessary?