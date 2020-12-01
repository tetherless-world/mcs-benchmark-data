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
        "TestArgs",
        [("benchmark_name", str), ("using_test_data", bool), ("root_path", Path)],
    )

    test_args = TestArgs("snazzy_new_benchmark", True, tmpdir)

    CreateBenchmarkPipelineCommand(args=test_args)()

    assert_benchmark_pipeline_compiles(
        root_path=tmpdir, benchmark_name=test_args.benchmark_name
    )
