from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineTemplateMetadata:
    """
    Information about the pipeline file necessary to create a file from a template
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
                "benchmark_name_benchmark_pipeline.py.template"
                if self.submission_name is None
                else "submission_name_benchmark_name_submission_pipeline.py.template"
            ),
        )
        object.__setattr__(
            self,
            "dest_file_name",
            (
                f"{self.benchmark_name}_benchmark_pipeline.py"
                if self.submission_name is None
                else f"{self.submission_name}_{self.benchmark_name}_submission_pipeline.py"
            ),
        )

        object.__setattr__(
            self,
            "dest_file_path_from_root",
            (
                "mcs_benchmark_data/pipelines"
                / Path(self.benchmark_name)
                / self.dest_file_name
            ),
        )
