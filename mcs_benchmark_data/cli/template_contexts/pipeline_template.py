from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from mcs_benchmark_data.cli.template_contexts.template import Template


class PipelineTemplate(Template):
    """
    Information about the pipeline file necessary to create a file from a template
    """

    def __init__(self, *, benchmark_name: str, submission_name: Optional[str] = None):
        context = Template.Context(
            benchmark_name=benchmark_name, submission_name=submission_name
        )
        dest_file_name = (
            f"{benchmark_name}_benchmark_pipeline.py"
            if submission_name is None
            else f"{submission_name}_{benchmark_name}_submission_pipeline.py"
        )
        template_file_name = (
            "benchmark_name_benchmark_pipeline.py.template"
            if submission_name is None
            else "submission_name_benchmark_name_submission_pipeline.py.template"
        )
        dest_file_path_from_root = (
            "mcs_benchmark_data/pipelines" / Path(benchmark_name) / dest_file_name
        )
        Template.__init__(
            self,
            context=context,
            dest_file_name=dest_file_name,
            template_file_name=template_file_name,
            dest_file_path_from_root=dest_file_path_from_root,
        )
