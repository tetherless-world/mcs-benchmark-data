from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from mcs_benchmark_data.cli.template_contexts.file_context import FileContext


@dataclass(init=True)
class TestTemplateContext(FileContext):
    """
    Information about the test file necessary to create a file from a template
    """

    def __init__(self, benchmark_name, submission_name=None):
        self.benchmark_name = benchmark_name
        self.submission_name = submission_name
        self.template_name = (
            "benchmark_name_pipeline_test.py.template"
            if self.submission_name is None
            else "submission_name_benchmark_name_pipeline_test.py.template"
        )
        self.dest_file_name = (
            f"{self.benchmark_name}_pipeline_test.py"
            if self.submission_name is None
            else f"{self.submission_name}_{self.benchmark_name}_pipeline_test.py"
        )
        self.dest_file_path_from_root = (
            "tests/mcs_benchmark_data_test/pipelines"
            / Path(self.benchmark_name)
            / self.dest_file_name
        )
