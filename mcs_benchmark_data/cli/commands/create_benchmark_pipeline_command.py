import os
import sys
import importlib
import stringcase as sc
from configargparse import ArgParser
from pathlib import Path
from string import Template

from mcs_benchmark_data.path import ROOT_DIR_PATH
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

        self._make_benchmark_directories(
            root_path=ROOT_DIR_PATH, benchmark_name=benchmark_name
        )

        self._create_files_from_template(
            root_path=ROOT_DIR_PATH, benchmark_name=benchmark_name, data_dir=data_dir
        )

    def _make_benchmark_directories(self, root_path: Path, benchmark_name: str):

        for dataset_type in DatasetType:

            self._make_new_directory(
                file_path=Path(
                    root_path
                    / "data"
                    / benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
                need_init=False,
            )

            self._make_new_directory(
                file_path=Path(
                    root_path
                    / "test_data"
                    / benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
                need_init=False,
            )

        self._logger.info(
            """6 new directories have been made for the dev, train, and test datasets of the new benchmark.\n
            Please add the proper data files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.\n
            Additionally, edit the metadata.json files in ./data/%s and ./test_data/%s by filling in the names of the benchmark authors.""",
            benchmark_name,
            benchmark_name,
        )

        # Make pipeline directory

        path_to_pipeline = (
            root_path / "mcs_benchmark_data" / "pipelines" / benchmark_name
        )

        self._make_new_directory(file_path=path_to_pipeline, need_init=True)

        path_to_tests = (
            root_path
            / "tests"
            / "mcs_benchmark_data_test"
            / "pipelines"
            / benchmark_name
        )

        self._make_new_directory(file_path=path_to_tests, need_init=True)
