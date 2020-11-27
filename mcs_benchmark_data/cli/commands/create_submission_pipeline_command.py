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
    def add_arguments(self, arg_parser: ArgParser, add_parent_args):
        arg_parser.add_argument(
            "--benchmark-name",
            help="name of the benchmark the submission was tested against (in snake_case)",
        )
        arg_parser.add_argument(
            "--submission-name",
            help="name of the model that the submission was made from (in snake_case)",
        )
        arg_parser.add_argument(
            "--using-test-data",
            help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
        )

    def __call__(self, args):

        benchmark_name = args.benchmark_name

        submission_name = args.submission_name

        using_test_data = args.using_test_data

        if not benchmark_name == sc.snakecase(benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )
        if not submission_name == sc.snakecase(submission_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if not Path(
            ROOT_DIR_PATH / "mcs_benchmark_data/pipelines" / benchmark_name
        ).exists():
            raise FileNotFoundError(
                "The benchmark that corresponds to the given benchmark name does not have an existing pipeline. Please follow the steps in the README to add the pipeline before proceeding with the submission."
            )

        if using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        is_first_submission = self.__make_submission_directories(
            root_path=ROOT_DIR_PATH,
            benchmark_name=benchmark_name,
            submission_name=submission_name,
        )

        self.__create_files_from_template(
            root_path=ROOT_DIR_PATH,
            benchmark_name=benchmark_name,
            submission_name=submission_name,
            data_dir=data_dir,
            is_first_submission=is_first_submission,
        )

    def __create_files_from_template(
        self,
        *,
        root_path: Path,
        benchmark_name: str,
        submission_name: str,
        data_dir: str,
        is_first_submission: bool,
    ):

        format_args = {
            "benchmark_name": benchmark_name,
            "BenchmarkName": sc.capitalcase(benchmark_name),
            "submission_name": submission_name,
            "SubmissionName": sc.capitalcase(submission_name),
            "data_dir": data_dir,
        }

        self._create_files_from_template(
            root_path=root_path,
            benchmark_name=benchmark_name,
            submission_name=submission_name,
            data_dir=data_dir,
            format_args=format_args,
            is_first_submission=is_first_submission,
        )

    def __make_submission_directories(
        self, root_path: Path, benchmark_name: str, submission_name: str
    ) -> bool:

        data_path = Path(f"data/{benchmark_name}/submissions")

        submission_data_path = root_path / data_path

        is_first_submission = not bool(
            os.path.exists(submission_data_path / "submissions_metadata.jsonl")
        )

        self.make_new_directory(
            file_path=Path(submission_data_path / f"{submission_name}"), need_init=False
        )
        self.make_new_directory(
            file_path=Path(root_path / f"test_{data_path}/{submission_name}"),
            need_init=False,
        )

        if is_first_submission:
            self._logger.info(
                """Since this is not the first submission for this benchmark, please edit the file ./data/%s/submissions/submissions_metadata.jsonl and the same file in the /test_data/%s/submissions/ directory.\n
            Edit the files by copying the last entry and pasting it directly below. Edit the entry according to the information from the new submission.""",
                benchmark_name,
                benchmark_name,
            )
        else:
            self._logger.info(
                """The submission metadata files have been created at the following paths:\n 
                 - ./data/%s/submissions/submissions_metadata.jsonl\n 
                 - ./test_data/%s/submissions/submissions_metadata.jsonl\n
            Edit the files by entering in the missing information that corresponds to the submission.""",
                benchmark_name,
                benchmark_name,
            )

        return is_first_submission
