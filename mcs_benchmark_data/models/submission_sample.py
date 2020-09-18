from mcs_benchmark_data.models.model import Model

class Submission(Model):
    '''An entry in a submission dataset (i.e. prediction)'''
    type: str
    includedInDataset: str
    value: int
    about: str