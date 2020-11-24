from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(init=True)
class FileContext:
    """
    Information about a file necessary to create a file from a template
    """

    benchmark_name: str
    submission_name: Optional[str] = None
    template_name: Optional[str] = None
    dest_file_name: Optional[str] = None
    dest_file_path_from_root: Optional[Path] = None
