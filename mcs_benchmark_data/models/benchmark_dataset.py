from mcs_benchmark_data.models.model import Model


class BenchmarkDataset(Model):
    '''A file containing elements (questions, answers, context, observations, ...) of a benchmark'''
    '''Sub-classes: BenchmarkDevDataset, BenchmarkTestDataset, BenchmarkTrainingDataset'''
    name: str