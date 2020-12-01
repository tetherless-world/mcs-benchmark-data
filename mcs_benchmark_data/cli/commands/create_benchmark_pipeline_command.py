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
    """
    Creates the directories and files necessary for a benchmark pipeline
    """

    def __init__(self, args: dict, **kwds):
        _Command.__init__(self, **kwds)
        self.benchmark_name = args.benchmark_name
        self.submission_name = None

        self.using_test_data = args.using_test_data
        self.root_path = args.root_path

    @classmethod
    def add_arguments(self, arg_parser: ArgParser):
        pass

    def __call__(self):

        if not self.benchmark_name == sc.snakecase(self.benchmark_name):
            raise ValueError(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )

        if self.using_test_data:
            data_dir = "TEST_DATA_DIR_PATH"
        else:
            data_dir = "DATA_DIR_PATH"

        self._make_benchmark_directories()

        self._create_files_from_template(data_dir=data_dir)

    def _make_benchmark_directories(self):
        """
        Make the directories needed for the benchmark pipeline
        :param root_path: the path to the mcs-benchmark-data directory
        :param benchmark_name: the name of the benchmark
        """
        for dataset_type in DatasetType:

            self._make_new_directory(
                file_path=Path(
                    self.root_path
                    / "data"
                    / self.benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
                need_init=False,
            )

            self._make_new_directory(
                file_path=Path(
                    self.root_path
                    / "test_data"
                    / self.benchmark_name
                    / "datasets"
                    / dataset_type.value
                ),
                need_init=False,
            )

        self._logger.info(
            """6 new directories have been made for the dev, train, and test datasets of the new benchmark.
            Please add the proper data files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.
            Additionally, edit the metadata.json files in ./data/%s and ./test_data/%s by filling in the names of the benchmark authors.""",
            self.benchmark_name,
            self.benchmark_name,
        )

        # Make pipeline directory

        path_to_pipeline = (
            self.root_path / "mcs_benchmark_data" / "pipelines" / self.benchmark_name
        )

        self._make_new_directory(file_path=path_to_pipeline, need_init=True)

        path_to_tests = (
            self.root_path
            / "tests"
            / "mcs_benchmark_data_test"
            / "pipelines"
            / self.benchmark_name
        )

        self._make_new_directory(file_path=path_to_tests, need_init=True)
