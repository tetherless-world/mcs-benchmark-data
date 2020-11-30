from enum import Enum


class TemplateType(Enum):
    """
    Types of benchmark/submission file templates
    """

    PIPELINE = "pipeline"
    TRANSFORMER = "transformer"
    TEST = "test"
    METADATA = "metadata"
