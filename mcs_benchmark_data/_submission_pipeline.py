from mcs_benchmark_data._pipeline import _Pipeline


class _SubmissionPipeline(_Pipeline):
    DATASET_TYPE_DEFAULT = "dev"

    @classmethod
    def add_arguments(cls, arg_parser) -> None:
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--dataset-type", default=cls.DATASET_TYPE_DEFAULT)
