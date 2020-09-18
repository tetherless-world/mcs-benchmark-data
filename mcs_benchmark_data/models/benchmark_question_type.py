from enum import auto, Enum


class BenchmarkQuestionType(str, Enum):
    '''The type of a benchmark sample (i.e. multiple choice, true/false).'''
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"
    ##Should I include extra category here for multiple choice based on passage?