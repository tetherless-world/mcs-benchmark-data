import logging
import importlib
from abc import ABC, abstractmethod
from configargparse import ArgParser
from types import FunctionType

from typing import Optional
from pathlib import Path
from string import Template
from mcs_benchmark_data.path import ROOT_DIR_PATH

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

    def __init__(
        self,
        benchmark_name: str,
        submission_name: str = None,
        using_test_data: bool = False,
        **kwds,
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.benchmark_name = benchmark_name
        self.submission_name = submission_name
        self.using_test_data = using_test_data

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        """
        Add sub-command-specific arguments to the argparse (sub-) ArgParser
        """

    @abstractmethod
    def __call__(self) -> None:
        """
        Invoke .__call__ with the parsed arguments
        """

    def _make_new_directory(self, *, file_path: Path, need_init: bool):
        """
        Make a new directory at the path specified.
        :param file_path: the path to the file/directory
        :param need_init: true if the directory needs an __init__ file created
        """

        if Path(file_path).exists():
            raise FileExistsError(f"The directory at {file_path} already exists.")

        Path(file_path).mkdir(parents=True)

        if need_init:

            Path(file_path / "__init__.py").touch()

        self._logger.info("The directory %s has been created.", file_path)

    def _create_files_from_template(
        self,
        *,
        root_path: Path,
        data_dir: str,
        is_first_submission: Optional[bool] = None,
    ):

        """
        Create all of the necessary pipeline files for a benchmark/submission from tempaltes
        :param root_path: the path from root to the mcs-benchmark-data directory
        :param data_dir: the directory being used for testing (i.e. DATA_DIR_PATH or TEST_DATA_DIR_PATH)
        :param is_first_submission: true if the submission is the first submission for the benchmark
        """

        for template_type in TemplateType:

            # Do not re-create the submission_metadata file if it already
            # exists for other submission(s) for this benchmark
            if (
                template_type == TemplateType.METADATA
                and is_first_submission is not None
                and is_first_submission == False
            ):
                continue

            template_module = importlib.import_module(
                f"mcs_benchmark_data.cli.template_contexts.{template_type.value}_template"
            )
            TemplateDataclass = getattr(
                template_module, f"{template_type.value.capitalize()}Template"
            )

            template_metadata = TemplateDataclass(
                benchmark_name=self.benchmark_name, submission_name=self.submission_name
            )

            # Update the template for the benchmark/submission provided
            template_metadata.execute(root_path=root_path, data_dir=data_dir)

            self._logger.info(
                "A %s file has been created at %s",
                template_metadata.__class__.__name__,
                ROOT_DIR_PATH / template_metadata.dest_file_path_from_root,
            )

            if template_type == TemplateType.METADATA:

                self._logger.info(
                    "A %s file has been created at %s",
                    template_type.value,
                    root_path
                    / f"test_{str(template_metadata.dest_file_path_from_root)}",
                )
