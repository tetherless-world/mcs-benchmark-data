import os
import re
import sys
import importlib

import humps

from typing import Optional

from pathlib import Path

from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.template_type import TemplateType


class PipelineCreator:
    def __init__(
        self,
        *,
        benchmark_name: str,
        submission_name: Optional[str] = None,
    ):
        self.curr_path = Path(__file__).parent

        self.benchmark_name = benchmark_name
        self.submission_name = submission_name

    def create_files_from_template(self, is_first_submission: Optional[bool] = None):

        path_to_templates = self.curr_path / "templates"

        format_args = {
            "benchmark_name": self.benchmark_name,
            "BenchmarkName": humps.pascalize(self.benchmark_name),
        }

        if submission_name is not None:
            add_format_args = {
                "submission_name": self.submission_name,
                "SubmissionName": humps.pascalize(self.submission_name),
            }
            format_args.update(add_format_args)

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
                benchmark_name=self.benchmark_name, submission_name=self.submission_name
            )

            with open(
                path_to_templates / template_metadata.template_name
            ) as template_file:
                template_str = template_file.read()

            formatted_str = template_str.format(**format_args)

            with open(
                self.curr_path / template_metadata.dest_file_path_from_root, "w"
            ) as fp:
                fp.write(formatted_str)

            if template_type == TemplateType.METADATA:

                os.symlink(
                    self.curr_path / template_metadata.dest_file_path_from_root,
                    self.curr_path
                    / f"test_{str(template_metadata.dest_file_path_from_root)}",
                )

    def make_benchmark_directories(self):

        for dataset_type in DatasetType:
            os.makedirs(
                self.curr_path
                / "data"
                / self.benchmark_name
                / "datasets"
                / dataset_type.value
            )
            os.makedirs(
                self.curr_path
                / "test_data"
                / self.benchmark_name
                / "datasets"
                / dataset_type.value
            )

        print(
            f"""6 new directories have been made for the dev, train, and test datasets of the new benchmark in the following paths:\n
        -./data/{self.benchmark_name}/datasets/{dataset_type.value}\n
        -./test_data/{self.benchmark_name}/datasets/{dataset_type.value}\n
            Please add the proper data files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.\n
            Additionally, edit the metadata.json file from ./data/benchmark_name by filling in the names of the benchmark authors.\n"""
        )

        # Make pipeline directory

        path_to_pipeline = (
            self.curr_path / "mcs_benchmark_data" / "pipelines" / self.benchmark_name
        )

        os.makedirs(path_to_pipeline)

        Path(path_to_pipeline / "__init__.py").touch()

        print(
            f"""A new directory has been made for the pipeline files of the new benchmark at the following path:\n
        -./mcs_benchmark_data/pipelines/{self.benchmark_name}\n
        Please edit the {self.benchmark_name}_benchmark_* files according to the steps specified in the README.md"""
        )

        path_to_tests = (
            self.curr_path
            / "tests"
            / "mcs_benchmark_data_test"
            / "pipelines"
            / self.benchmark_name
        )

        # Make test directory
        os.makedirs(path_to_tests)

        Path(path_to_tests / "__init__.py").touch()

        print(
            f"""A new directory has been made for the pipeline test files of the new benchmark at the following path:\n
        -./tests/mcs_benchmark_data_test/pipelines/{self.benchmark_name}\n
        Please edit the benchmark test file according to the steps specified in the README.md"""
        )

        self.create_files_from_template()

    def make_submission_directories(self):

        data_path = Path(f"data/{self.benchmark_name}/submissions")

        submission_data_path = self.curr_path / data_path

        is_first_submission = not bool(
            os.path.exists(submission_data_path / "submissions_metadata.jsonl")
        )

        os.makedirs(submission_data_path / f"{self.submission_name}")

        os.makedirs(self.curr_path / f"test_{data_path}/{self.submission_name}")

        if is_first_submission:
            print(
                f"""Since this is not the first submission for this benchmark, please edit the file ./data/{self.benchmark_name}/submissions/submissions_metadata.jsonl.\n
            Edit the file by copying the last entry and pasting it directly below. Edit the entry according to the information from the new submission.\n"""
            )

        print(
            f"""The submission pipeline files have been added to the following directory:\n
        -./mcs_benchmark_data/pipelines/{self.benchmark_name}\n
        Please edit the {self.submission_name}_{self.benchmark_name}_submission_* files according to the steps specified in the README.md"""
        )

        print(
            f"""The submission pipeline test files have been added to the following directory:\n
        -./tests/mcs_benchmark_data_test/pipelines/{self.benchmark_name}\n
        Please edit the {self.submission_name}_{self.benchmark_name}_submission_pipeline_test.py file according to the steps specified in the README.md"""
        )

        self.create_files_from_template(
            is_first_submission=is_first_submission,
        )


if __name__ == "__main__":

    args = sys.argv

    if len(args) <= 1 or len(args) > 4:
        print(
            "An incorrect number of arguments was specified. Refer to the README.md file for how to properly execute the script."
        )
        sys.exit()

    option = sys.argv[1]

    if option == "--benchmark":

        benchmark_name = sys.argv[2]

        submission_name = None

        if not humps.is_snakecase(benchmark_name):
            print(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )
            sys.exit()

        pc = PipelineCreator(
            benchmark_name=benchmark_name, submission_name=submission_name
        )

        pc.make_benchmark_directories()

    elif option == "--submission":

        submission_name = sys.argv[2]

        benchmark_name = sys.argv[3]

        if not os.path.exists(Path(__file__).parent / f"data/{benchmark_name}"):
            print(
                "Please add the benchmark directories/files before adding a submission. Refer to the README.md for further instructions."
            )
            sys.exit()

        pc = PipelineCreator(
            benchmark_name=benchmark_name, submission_name=submission_name
        )

        pc.make_submission_directories()

    else:
        print(
            "The first argument must be either '--benchmark' or '--submission'. Please refer to the README.md for further instructions."
        )
