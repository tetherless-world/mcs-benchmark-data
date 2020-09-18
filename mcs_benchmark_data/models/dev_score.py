from mcs_benchmark_data.models.model import Model

class DevScore(Model):
    '''Score of a system's correct predictions against a dev benchmark dataset'''
    name: str
    value: str