from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MetadataTemplateMetadata:
    """
    Information about the metadata file necessary to create a file from a template
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
                "metadata.json.template"
                if self.submission_name is None
                else "submissions_metadata.jsonl.template"
            ),
        )
        object.__setattr__(
            self,
            "dest_file_name",
            (
                "metadata.json"
                if self.submission_name is None
                else "submissions_metadata.jsonl"
            ),
        )

        object.__setattr__(
            self,
            "dest_file_path_from_root",
            (
                "data" / Path(self.benchmark_name) / self.dest_file_name
                if self.submission_name is None
                else "data"
                / Path(self.benchmark_name)
                / "submissions"
                / Path(self.dest_file_name)
            ),
        )
