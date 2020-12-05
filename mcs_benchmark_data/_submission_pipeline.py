from pathlib import Path

from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.path import DATA_DIR_PATH


class _SubmissionPipeline(_Pipeline):
    DATASET_TYPE_DEFAULT = "dev"

    def _loaded_file_path(
        self,
        *,
        data_dir_path: Path = DATA_DIR_PATH,
        submission_id: str,
        benchmark_id: str,
    ) -> Path:
        return (
            data_dir_path
            / benchmark_id
            / "loaded"
            / f"{self.DATASET_TYPE_DEFAULT}_{submission_id}_{benchmark_id}_submission.ttl.bz2"
        )

    @classmethod
    def add_arguments(cls, arg_parser) -> None:
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--dataset-type", default=cls.DATASET_TYPE_DEFAULT)
