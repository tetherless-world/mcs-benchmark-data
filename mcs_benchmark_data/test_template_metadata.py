from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TestTemplateMetadata:
    """
    Information about the test file necessary to create a file from a template
    """

    benchmark_name: str
    submission_name: Optional[str] = None
    template_name: Optional[str] = None
    dest_file_name: Optional[str] = None
    dest_file_path_from_root: Optional[Path] = None

    def __post_init__(self):
        object.__setattr__(
            self,
            "template_name",
            (
                "benchmark_name_pipeline_test.py.template"
                if self.submission_name is None
                else "submission_name_benchmark_name_pipeline_test.py.template"
            ),
        )
        object.__setattr__(
            self,
            "dest_file_name",
            (
                f"{self.benchmark_name}_pipeline_test.py"
                if self.submission_name is None
                else f"{self.submission_name}_{self.benchmark_name}_pipeline_test.py"
            ),
        )

        object.__setattr__(
            self,
            "dest_file_path_from_root",
            (
                "tests/mcs_benchmark_data_test/pipelines"
                / Path(self.benchmark_name)
                / self.dest_file_name
            ),
        )
