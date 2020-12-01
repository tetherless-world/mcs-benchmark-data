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

    TestArgs = NamedTuple(
        "TestArgs",
        [
            ("benchmark_name", str),
            ("submission_name", str),
            ("using_test_data", bool),
            ("root_path", Path),
        ],
    )

    test_args = TestArgs("snazzy_new_benchmark", "kagnet", True, tmpdir)

    CreateBenchmarkPipelineCommand(args=test_args)()

    CreateSubmissionPipelineCommand(args=test_args)()

    assert_submission_pipeline_compiles(
        root_path=tmpdir,
        benchmark_name=test_args.benchmark_name,
        submission_name=test_args.submission_name,
    )

    test_args_new = TestArgs("snazzy_new_benchmark", "roberta", True, tmpdir)

    CreateSubmissionPipelineCommand(args=test_args_new)()

    assert_submission_pipeline_compiles(
        root_path=tmpdir,
        benchmark_name=test_args_new.benchmark_name,
        submission_name=test_args_new.submission_name,
    )
