from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from mcs_benchmark_data.cli.template_contexts.file_context import FileContext


@dataclass(init=True)
class MetadataTemplateContext(FileContext):
    """
    Information about the metadata file necessary to create a file from a template
    """

    def __init__(self, benchmark_name, submission_name=None):
        self.benchmark_name = benchmark_name
        self.submission_name = submission_name
        self.template_name = (
            "metadata.json.template"
            if self.submission_name is None
            else "submissions_metadata.jsonl.template"
        )
        self.dest_file_name = (
            "metadata.json"
            if self.submission_name is None
            else "submissions_metadata.jsonl"
        )
        self.dest_file_path_from_root = (
            "data" / Path(self.benchmark_name) / self.dest_file_name
            if self.submission_name is None
            else "data"
            / Path(self.benchmark_name)
            / "submissions"
            / Path(self.dest_file_name)
        )
