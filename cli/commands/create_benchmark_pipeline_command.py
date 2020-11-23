import os
import sys
import importlib
import humps
from configargparse import ArgParser
from pathlib import Path
from string import Template

from mcs_benchmark_data.path import DATA_DIR_PATH, TEST_DATA_DIR_PATH
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.template_type import TemplateType

from cli.commands._command import _Command


class CreateBenchmarkPipelineCommand(_Command):
    def add_arguments(self, arg_parser: ArgParser, add_parent_args):
        arg_parser.add_argument(
            "--benchmark_name", help="name of the new benchmark (in snake_case)"
        )
        arg_parser.add_argument(
            "--using-test-data",
            help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
        )

    def __call__(self, args):

        root_path = Path(__file__).parent.parent.parent

        benchmark_name = args.benchmark_name

        using_test_data = args.using_test_data

        if not humps.is_snakecase(benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        self.__make_benchmark_directories(
            root_path=root_path, benchmark_name=benchmark_name
        )

        self.__create_files_from_template(
            root_path=root_path, benchmark_name=benchmark_name, data_dir=data_dir
        )

    def __create_files_from_template(
        self, root_path: Path, benchmark_name: str, data_dir: str
    ):

        path_to_templates = root_path / "templates"

        format_args = {
            "benchmark_name": benchmark_name,
            "BenchmarkName": humps.pascalize(benchmark_name),
            "data_dir": data_dir,
        }

        for template_type in TemplateType:

            template_module = importlib.import_module(
                f"mcs_benchmark_data.{template_type.value}_template_metadata"
            )
            TemplateDataclass = getattr(
                template_module, f"{template_type.value.capitalize()}TemplateMetadata"
            )

            template_metadata = TemplateDataclass(benchmark_name=benchmark_name)

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

    def __make_benchmark_directories(self, root_path: Path, benchmark_name: str):

        root_path = Path(__file__).parent.parent.parent

        for dataset_type in DatasetType:
            os.makedirs(
                root_path / "data" / benchmark_name / "datasets" / dataset_type.value
            )
            os.makedirs(
                root_path
                / "test_data"
                / benchmark_name
                / "datasets"
                / dataset_type.value
            )

        self._logger.info(
            f"""6 new directories have been made for the dev, train, and test datasets of the new benchmark in the following paths:\n
        -./data/{benchmark_name}/datasets/{dataset_type.value}\n
        -./test_data/{benchmark_name}/datasets/{dataset_type.value}\n
            Please add the proper data files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.\n
            Additionally, edit the metadata.json file from ./data/benchmark_name by filling in the names of the benchmark authors.\n"""
        )

        # Make pipeline directory

        path_to_pipeline = (
            root_path / "mcs_benchmark_data" / "pipelines" / benchmark_name
        )

        os.makedirs(path_to_pipeline)

        Path(path_to_pipeline / "__init__.py").touch()

        self._logger.info(
            f"""A new directory has been made for the pipeline files of the new benchmark at the following path:\n
        -./mcs_benchmark_data/pipelines/{benchmark_name}\n
        Please edit the {benchmark_name}_benchmark_* files according to the steps specified in the README.md"""
        )

        self._logger.info(
            f"""The benchmark pipeline files have been added to the following directory:\n
        -./mcs_benchmark_data/pipelines/{benchmark_name}\n
        Please edit the {benchmark_name}_submission_* files according to the steps specified in the README.md"""
        )

        path_to_tests = (
            root_path
            / "tests"
            / "mcs_benchmark_data_test"
            / "pipelines"
            / benchmark_name
        )

        # Make test directory
        os.makedirs(path_to_tests)

        Path(path_to_tests / "__init__.py").touch()

        self._logger.info(
            f"""The benchmark pipeline test files have been added to the following directory:\n
        -./tests/mcs_benchmark_data_test/pipelines/{benchmark_name}\n
        Please edit the {benchmark_name}_submission_pipeline_test.py file according to the steps specified in the README.md"""
        )
