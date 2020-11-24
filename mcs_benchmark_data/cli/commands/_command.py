import logging
import importlib
from abc import ABC, abstractmethod
from configargparse import ArgParser
from types import FunctionType

from typing import Optional
from pathlib import Path
from string import Template

from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.cli.template_type import TemplateType


class _Command(ABC):
    """
    A command-line (sub-)command.
    For each _Command, the command-line entrypoint (main):
    1) Creates an ArgumentParser sub-command parser
    2) Calls .add_arguments to add sub-command specific arguments to this sub-parser
    If the sub-command is invoked, then
    3) Invoke .__call__ with the parsed arguments
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def add_arguments(
        self, arg_parser: ArgParser, add_parent_args: FunctionType
    ) -> None:
        """
        Add sub-command-specific arguments to the argparse (sub-) ArgParser
        """

    @abstractmethod
    def __call__(self, args) -> None:
        """
        Invoke .__call__ with the parsed arguments
        """

    def _create_files_from_template(
        self,
        *,
        root_path: Path,
        benchmark_name: str,
        data_dir: str,
        format_args: dict,
        submission_name: Optional[str] = None,
        is_first_submission: Optional[bool] = None,
    ):

        repo_root = Path(__file__).parent.parent.parent.parent

        path_to_templates = repo_root / "mcs_benchmark_data" / "cli" / "templates"

        for template_type in TemplateType:

            if (
                template_type == TemplateType.METADATA
                and is_first_submission is not None
                and is_first_submission == False
            ):
                continue

            template_module = importlib.import_module(
                f"mcs_benchmark_data.cli.template_contexts.{template_type.value}_template_context"
            )
            TemplateDataclass = getattr(
                template_module, f"{template_type.value.capitalize()}TemplateContext"
            )

            template_metadata = TemplateDataclass(
                benchmark_name=benchmark_name, submission_name=submission_name
            )

            with open(
                path_to_templates / template_metadata.template_name
            ) as template_file:
                template_str = template_file.read()

            if template_type == TemplateType.METADATA:
                temp = Template(template_str)
                formatted_str = temp.substitute(**format_args)

            else:
                formatted_str = template_str.format(**format_args)

            if Path(root_path / template_metadata.dest_file_path_from_root).exists():
                raise FileExistsError(
                    f"The file at {root_path / template_metadata.dest_file_path_from_root} already exists."
                )

            with open(
                root_path / template_metadata.dest_file_path_from_root, "w"
            ) as fp:
                fp.write(formatted_str)

            if template_type == TemplateType.METADATA:

                if Path(
                    root_path
                    / f"test_{str(template_metadata.dest_file_path_from_root)}"
                ).exists():
                    raise FileExistsError(
                        f"The file at {root_path}/test_{str(template_metadata.dest_file_path_from_root)} already exists."
                    )

                with open(
                    root_path
                    / f"test_{str(template_metadata.dest_file_path_from_root)}",
                    "w",
                ) as fp:
                    fp.write(formatted_str)
