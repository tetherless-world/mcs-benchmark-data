import os
import sys
import importlib
import stringcase as sc
from typing import Optional
from configargparse import ArgParser
from pathlib import Path
from string import Template

from mcs_benchmark_data.path import ROOT_DIR_PATH
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.cli.template_type import TemplateType

from mcs_benchmark_data.cli.commands._command import _Command


class CreateSubmissionPipelineCommand(_Command):
    """
    Creates the directories and files necessary for a benchmark submission pipeline
    """

    def __init__(
        self,
        *,
        benchmark_name: str,
        submission_name: str,
        using_test_data: bool,
        root_path: Path,
        **kwds,
    ):
        _Command.__init__(self, **kwds)
        self.benchmark_name = benchmark_name
        self.submission_name = submission_name

        self.using_test_data = using_test_data
        self.root_path = root_path

    @classmethod
    def add_arguments(self, arg_parser: ArgParser):
        arg_parser.add_argument(
            "--benchmark-name",
            required=True,
            help="name of the benchmark the submission was tested against (in snake_case)",
        )
        arg_parser.add_argument(
            "--submission-name",
            required=True,
            help="name of the model that the submission was made from (in snake_case)",
        )
        arg_parser.add_argument(
            "--using-test-data",
            help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
        )

    def __call__(self):

        if not self.benchmark_name == sc.snakecase(self.benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )
        if not self.submission_name == sc.snakecase(self.submission_name):
            raise ValueError(
                "This submission name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if not Path(
            self.root_path / "mcs_benchmark_data/pipelines" / self.benchmark_name
        ).exists():
            raise FileNotFoundError(
                "The benchmark that corresponds to the given benchmark name does not have an existing pipeline. Please follow the steps in the README to add the pipeline before proceeding with the submission."
            )

        if self.using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        is_first_submission = self._make_submission_directories()

        self._create_files_from_template(
            data_dir=data_dir, is_first_submission=is_first_submission
        )

    def _make_submission_directories(
        self,
    ) -> bool:
        """
        Make the directories needed for the submission pipeline
        :return: true if this is the first submission for the benchmark specified
        """
        data_path = Path(f"data/{self.benchmark_name}/submissions")

        submission_data_path = self.root_path / data_path

        is_first_submission = not bool(
            Path(submission_data_path / "submissions_metadata.jsonl").exists()
        )

        self._make_new_directory(
            file_path=Path(submission_data_path / f"{self.submission_name}"),
            need_init=False,
        )
        self._make_new_directory(
            file_path=Path(self.root_path / f"test_{data_path}/{self.submission_name}"),
            need_init=False,
        )

        if not is_first_submission:
            self._logger.info(
                """Since this is not the first submission for this benchmark, please edit the file ./data/%s/submissions/submissions_metadata.jsonl and the same file in the /test_data/%s/submissions/ directory.
            Edit the files by copying the last entry and pasting it directly below. Edit the entry according to the information from the new submission.""",
                self.benchmark_name,
                self.benchmark_name,
            )
        else:
            self._logger.info(
                """\
        The submission metadata files have been created at the following paths: 
            - ./data/%s/submissions/submissions_metadata.jsonl 
            - ./test_data/%s/submissions/submissions_metadata.jsonl
        Edit the files by entering in the missing information that corresponds to the submission.""",
                self.benchmark_name,
                self.benchmark_name,
            )

        return is_first_submission
