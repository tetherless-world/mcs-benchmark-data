from typing import NamedTuple
from pathlib import Path
import py_compile

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH, DATA_DIR_PATH
from mcs_benchmark_data.dataset_type import DatasetType
from tests.mcs_benchmark_data_test.assertions import assert_benchmark_pipeline_compiles

from mcs_benchmark_data.cli.commands.create_benchmark_pipeline_command import (
    CreateBenchmarkPipelineCommand,
)


def test_create_benchmark_pipeline(tmpdir):

    TestArgs = NamedTuple(
        "TestArgs", [("benchmark_name", str), ("using_test_data", bool)]
    )

    test_args = TestArgs("snazzy_new_benchmark", True)

    CreateBenchmarkPipelineCommand(args=test_args, root_path=tmpdir)()

    # CreateBenchmarkPipelineCommand()._make_benchmark_directories(
    #     root_path=tmpdir, benchmark_name=test_args.benchmark_name
    # )

    # CreateBenchmarkPipelineCommand()._create_files_from_template(
    #     root_path=tmpdir,
    #     benchmark_name=test_args.benchmark_name,
    #     data_dir="TEST_DATA_DIR_PATH" if test_args.using_test_data else "DATA_DIR_PATH",
    # )

    assert_benchmark_pipeline_compiles(
        root_path=tmpdir, benchmark_name=test_args.benchmark_name
    )
