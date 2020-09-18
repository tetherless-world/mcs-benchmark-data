from enum import auto, Enum

class BenchmarkQuestionCategory(str, Enum):
    '''The category of a benchmark sample (i.e. temporal reasoning, temporal sequences ...)'''
    TEMPORAL_REASONING = "TEMPORAL_REASONING"
    TAXONOMIC_REASONING = "TAXONOMIC_REASONING"
    QUALITATIVE_REASONING = "QUALITATIVE_REASONING"
    TEMPORAL_SEQUENCES = "TEMPORAL_SEQUENCES"