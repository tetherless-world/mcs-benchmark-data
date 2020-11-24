from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from mcs_benchmark_data.cli.template_contexts.file_context import FileContext


@dataclass(init=True)
class TransformerTemplateContext(FileContext):
    """
    Information about the transformer file necessary to create a file from a template
    """

    def __init__(self, benchmark_name, submission_name=None):
        self.benchmark_name = benchmark_name
        self.submission_name = submission_name
        self.template_name = (
            "benchmark_name_benchmark_transformer.py.template"
            if self.submission_name is None
            else "submission_name_benchmark_name_submission_transformer.py.template"
        )
        self.dest_file_name = (
            f"{self.benchmark_name}_benchmark_transformer.py"
            if self.submission_name is None
            else f"{self.submission_name}_{self.benchmark_name}_submission_transformer.py"
        )
        self.dest_file_path_from_root = (
            "mcs_benchmark_data/pipelines"
            / Path(self.benchmark_name)
            / self.dest_file_name
        )