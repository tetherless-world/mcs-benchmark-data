import os
import sys
import importlib
import stringcase as sc
from configargparse import ArgParser
from pathlib import Path
from string import Template

from mcs_benchmark_data.path import DATA_DIR_PATH, TEST_DATA_DIR_PATH
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.cli.template_type import TemplateType

from mcs_benchmark_data.cli.commands._command import _Command


class CreateBenchmarkPipelineCommand(_Command):
    def add_arguments(self, arg_parser: ArgParser, add_parent_args):
        arg_parser.add_argument(
            "--benchmark-name", help="name of the new benchmark (in snake_case)"
        )
        arg_parser.add_argument(
            "--using-test-data",
            help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
        )

    def __call__(self, args):

        root_path = Path(__file__).parent.parent.parent.parent

        benchmark_name = args.benchmark_name

        using_test_data = args.using_test_data

        if not benchmark_name == sc.snakecase(benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        self.make_benchmark_directories(
            root_path=root_path, benchmark_name=benchmark_name
        )

        self.create_files_from_template(
            root_path=root_path, benchmark_name=benchmark_name, data_dir=data_dir
        )

    def create_files_from_template(
        self, *, root_path: Path, benchmark_name: str, data_dir: str, **kwds
    ):

        format_args = {
            "benchmark_name": benchmark_name,
            "BenchmarkName": sc.capitalcase(benchmark_name),
            "data_dir": data_dir,
        }

        self._create_files_from_template(
            root_path=root_path,
            benchmark_name=benchmark_name,
            data_dir=data_dir,
            format_args=format_args,
            **kwds,
        )

    def make_benchmark_directories(self, root_path: Path, benchmark_name: str):

        for dataset_type in DatasetType:

            Path(
                root_path / "data" / benchmark_name / "datasets" / dataset_type.value
            ).mkdir(parents=True)

            self._logger.info(
                "A new directory has been made at %s.\n",
                str(
                    root_path
                    / "data"
                    / benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
            )
            Path(
                root_path
                / "test_data"
                / benchmark_name
                / "datasets"
                / dataset_type.value
            ).mkdir(parents=True)

            self._logger.info(
                "A new directory has been made at %s.\n",
                str(
                    root_path
                    / "test_data"
                    / benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
            )

        self._logger.info(
            """6 new directories have been made for the dev, train, and test datasets of the new benchmark.\n
            Please add the proper data files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.\n
            Additionally, edit the metadata.json files in ./data/%s and ./test_data/%s by filling in the names of the benchmark authors.\n""",
            benchmark_name,
            benchmark_name,
        )

        # Make pipeline directory

        path_to_pipeline = (
            root_path / "mcs_benchmark_data" / "pipelines" / benchmark_name
        )

        Path(path_to_pipeline).mkdir(parents=True)

        Path(path_to_pipeline / "__init__.py").touch()

        self._logger.info(
            """A new directory has been made for the pipeline files of the new benchmark at the following path:\n
        -./mcs_benchmark_data/pipelines/%s\n
        Please edit the %s_benchmark_* files according to the steps specified in the README.md\n""",
            benchmark_name,
            benchmark_name,
        )

        self._logger.info(
            """The benchmark pipeline files have been added to the following directory:\n
        -./mcs_benchmark_data/pipelines/%s\n
        Please edit the %s_submission_* files according to the steps specified in the README.md\n""",
            benchmark_name,
            benchmark_name,
        )

        path_to_tests = (
            root_path
            / "tests"
            / "mcs_benchmark_data_test"
            / "pipelines"
            / benchmark_name
        )

        # Make test directory
        Path(path_to_tests).mkdir(parents=True)

        Path(path_to_tests / "__init__.py").touch()

        self._logger.info(
            """The benchmark pipeline test files have been added to the following directory:\n
        -./tests/mcs_benchmark_data_test/pipelines/%s\n
        Please edit the %s_submission_pipeline_test.py file according to the steps specified in the README.md""",
            benchmark_name,
            benchmark_name,
        )
