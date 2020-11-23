import os
import sys
import importlib
import humps
from typing import Optional
from configargparse import ArgParser
from pathlib import Path
from string import Template

from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.template_type import TemplateType

from cli.commands._command import _Command


class CreateSubmissionPipelineCommand(_Command):
    def add_arguments(self, arg_parser: ArgParser, add_parent_args):
        arg_parser.add_argument(
            "--benchmark_name",
            help="name of the benchmark the submission was tested against (in snake_case)",
        )
        arg_parser.add_argument(
            "--submission_name",
            help="name of the model that the submission was made from (in snake_case)",
        )
        arg_parser.add_argument(
            "--using-test-data",
            help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
        )

    def __call__(self, args):
        root_path = Path(__file__).parent.parent.parent

        benchmark_name = args.benchmark_name

        submission_name = args.submission_name

        using_test_data = args.using_test_data

        if not humps.is_snakecase(benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )
        if not humps.is_snakecase(submission_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        is_first_submission = self.__make_submission_directories(
            root_path=root_path,
            benchmark_name=benchmark_name,
            submission_name=submission_name,
        )

        self.__create_files_from_template(
            root_path=root_path,
            benchmark_name=benchmark_name,
            submission_name=submission_name,
            data_dir=data_dir,
            is_first_submission=is_first_submission,
        )

    def __create_files_from_template(
        self,
        root_path: Path,
        benchmark_name: str,
        submission_name: str,
        data_dir: str,
        is_first_submission: Optional[bool] = None,
    ):

        path_to_templates = root_path / "templates"

        format_args = {
            "benchmark_name": benchmark_name,
            "BenchmarkName": humps.pascalize(benchmark_name),
            "submission_name": submission_name,
            "SubmissionName": humps.pascalize(submission_name),
            "data_dir": data_dir,
        }

        for template_type in TemplateType:

            if template_type == TemplateType.METADATA and is_first_submission == False:
                continue

            template_module = importlib.import_module(
                f"mcs_benchmark_data.{template_type.value}_template_metadata"
            )
            TemplateDataclass = getattr(
                template_module, f"{template_type.value.capitalize()}TemplateMetadata"
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

            with open(
                root_path / template_metadata.dest_file_path_from_root, "w"
            ) as fp:
                fp.write(formatted_str)

            if template_type == TemplateType.METADATA:
                with open(
                    root_path
                    / f"test_{str(template_metadata.dest_file_path_from_root)}",
                    "w",
                ) as fp:
                    fp.write(formatted_str)

    def __make_submission_directories(
        self, root_path: Path, benchmark_name: str, submission_name: str
    ) -> bool:

        data_path = Path(f"data/{benchmark_name}/submissions")

        submission_data_path = root_path / data_path

        is_first_submission = not bool(
            os.path.exists(submission_data_path / "submissions_metadata.jsonl")
        )

        os.makedirs(submission_data_path / f"{submission_name}")

        os.makedirs(root_path / f"test_{data_path}/{submission_name}")

        self._logger.info(
            f"""The submission data directories have been created at the following paths:\n
            - ./data/{benchmark_name}/submissions\n 
            - ./test_data/{benchmark_name}/submissions\n
        Please add the corresponding data files according to the steps specified in the README.md"""
        )

        if is_first_submission:
            self._logger.info(
                f"""Since this is not the first submission for this benchmark, please edit the file ./data/{benchmark_name}/submissions/submissions_metadata.jsonl and the same file in the /test_data/{benchmark_name}/submissions/ directory.\n
            Edit the files by copying the last entry and pasting it directly below. Edit the entry according to the information from the new submission.\n"""
            )
        else:
            self._logger.info(
                f"""The submission metadata files have been created at the following paths:\n 
                 - ./data/{benchmark_name}/submissions/submissions_metadata.jsonl\n 
                 - ./test_data/{benchmark_name}/submissions/submissions_metadata.jsonl\n
            Edit the files by entering in the missing information that corresponds to the submission.\n"""
            )

        self._logger.info(
            f"""The submission pipeline files have been added to the following directory:\n
        -./mcs_benchmark_data/pipelines/{benchmark_name}\n
        Please edit the {submission_name}_{benchmark_name}_submission_* files according to the steps specified in the README.md"""
        )

        self._logger.info(
            f"""The submission pipeline test files have been added to the following directory:\n
        -./tests/mcs_benchmark_data_test/pipelines/{benchmark_name}\n
        Please edit the {submission_name}_{benchmark_name}_submission_pipeline_test.py file according to the steps specified in the README.md"""
        )

        return is_first_submission
