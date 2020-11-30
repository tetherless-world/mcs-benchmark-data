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
        [("benchmark_name", str), ("submission_name", str), ("using_test_data", bool)],
    )

    test_args = TestArgs("snazzy_new_benchmark", "kagnet", True)

    CreateBenchmarkPipelineCommand()._make_benchmark_directories(
        root_path=tmpdir, benchmark_name=test_args.benchmark_name
    )

    CreateSubmissionPipelineCommand()._make_submission_directories(
        root_path=tmpdir,
        benchmark_name=test_args.benchmark_name,
        submission_name=test_args.submission_name,
    )

    CreateSubmissionPipelineCommand()._create_files_from_template(
        root_path=tmpdir,
        benchmark_name=test_args.benchmark_name,
        submission_name=test_args.submission_name,
        data_dir="TEST_DATA_DIR_PATH" if test_args.using_test_data else "DATA_DIR_PATH",
    )

    assert_submission_pipeline_compiles(
        root_path=tmpdir,
        benchmark_name=test_args.benchmark_name,
        submission_name=test_args.submission_name,
    )

    test_args_new = TestArgs("snazzy_new_benchmark", "roberta", True)

    is_first_submission = (
        CreateSubmissionPipelineCommand()._make_submission_directories(
            root_path=tmpdir,
            benchmark_name=test_args_new.benchmark_name,
            submission_name=test_args_new.submission_name,
        )
    )

    CreateSubmissionPipelineCommand()._create_files_from_template(
        root_path=tmpdir,
        benchmark_name=test_args_new.benchmark_name,
        submission_name=test_args_new.submission_name,
        data_dir="TEST_DATA_DIR_PATH" if test_args.using_test_data else "DATA_DIR_PATH",
        is_first_submission=is_first_submission,
    )

    assert_submission_pipeline_compiles(
        root_path=tmpdir,
        benchmark_name=test_args_new.benchmark_name,
        submission_name=test_args_new.submission_name,
    )
