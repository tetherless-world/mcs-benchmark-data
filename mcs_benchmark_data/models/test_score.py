from mcs_benchmark_data.models.model import Model

class TestScore(Model):
    '''Score of a system's correct predictions against a test benchmark dataset'''
    name: str
    value: str