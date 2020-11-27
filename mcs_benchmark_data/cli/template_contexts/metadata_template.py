from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from mcs_benchmark_data.path import ROOT_DIR_PATH
from mcs_benchmark_data.cli.template_contexts.template import Template


@dataclass(init=True)
class MetadataTemplate(Template):
    """
    Information about the metadata file necessary to create a file from a template
    """

    def __init__(self, *, benchmark_name: str, submission_name: Optional[str] = None):
        context = Template.Context(
            benchmark_name=benchmark_name, submission_name=submission_name
        )
        dest_file_name = (
            "metadata.json" if submission_name is None else "submissions_metadata.jsonl"
        )
        template_file_name = (
            "metadata.json.template"
            if submission_name is None
            else "submissions_metadata.jsonl.template"
        )
        dest_file_path_from_root = (
            "data" / Path(benchmark_name) / dest_file_name
            if submission_name is None
            else "data" / Path(benchmark_name) / "submissions" / Path(dest_file_name)
        )

        Template.__init__(
            self,
            context=context,
            dest_file_name=dest_file_name,
            template_file_name=template_file_name,
            dest_file_path_from_root=dest_file_path_from_root,
        )

    def execute(self, *, root_path: Path, data_dir: str, force: Optional[bool] = False):

        formatted_str = Template.execute(
            self, root_path=root_path, data_dir=data_dir, force=force
        )

        self.write_new_file(
            root_path / f"test_{str(self.dest_file_path_from_root)}",
            formatted_str,
        )
