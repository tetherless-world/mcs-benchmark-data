from enum import Enum


class TemplateType(Enum):
    """
    Types of file templates
    """

    PIPELINE = "pipeline"
    TRANSFORMER = "transformer"
    TEST = "test"
    METADATA = "metadata"
