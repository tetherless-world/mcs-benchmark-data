from typing import NamedTuple
from pathlib import Path
import py_compile
import stringcase as sc

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH, DATA_DIR_PATH
from tests.mcs_benchmark_data_test.assertions import assert_submission_pipeline_compiles

from mcs_benchmark_data.cli.commands.create_benchmark_pipeline_command import (
    CreateBenchmarkPipelineCommand,
)
from mcs_benchmark_data.cli.commands.create_submission_pipeline_command import (
    CreateSubmissionPipelineCommand,
)


def test_create_submission_pipeline(tmpdir):

    benchmark_name = "snazzy_new_benchmark"
    submission_name_kag = "kagnet"
    using_test_data = True
    root_path = tmpdir

    CreateBenchmarkPipelineCommand(
        benchmark_name=benchmark_name,
        using_test_data=using_test_data,
        root_path=root_path,
    )()

    CreateSubmissionPipelineCommand(
        benchmark_name=benchmark_name,
        submission_name=submission_name_kag,
        using_test_data=using_test_data,
        root_path=root_path,
    )()

    assert_submission_pipeline_compiles(
        root_path=root_path,
        benchmark_name=benchmark_name,
        submission_name=submission_name_kag,
    )

    submission_name_rob = "roberta"

    CreateSubmissionPipelineCommand(
        benchmark_name=benchmark_name,
        submission_name=submission_name_rob,
        using_test_data=using_test_data,
        root_path=root_path,
    )()

    assert_submission_pipeline_compiles(
        root_path=tmpdir,
        benchmark_name=benchmark_name,
        submission_name=submission_name_rob,
    )
