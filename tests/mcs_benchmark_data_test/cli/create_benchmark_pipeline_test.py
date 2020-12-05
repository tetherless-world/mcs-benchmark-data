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

    benchmark_name = "snazzy_new_benchmark"
    using_test_data = True
    root_path = tmpdir

    CreateBenchmarkPipelineCommand(
        benchmark_name=benchmark_name,
        using_test_data=using_test_data,
        root_path=root_path,
    )()

    assert_benchmark_pipeline_compiles(
        root_path=root_path, benchmark_name=benchmark_name
    )
