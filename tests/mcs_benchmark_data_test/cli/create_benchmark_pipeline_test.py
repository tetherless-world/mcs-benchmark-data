from typing import NamedTuple
from pathlib import Path

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH, DATA_DIR_PATH
from mcs_benchmark_data.dataset_type import DatasetType

from mcs_benchmark_data.cli.commands.create_benchmark_pipeline_command import (
    CreateBenchmarkPipelineCommand,
)


def test_create_benchmark_pipeline(tmpdir):

    TestArgs = NamedTuple(
        "TestArgs", [("benchmark_name", str), ("using_test_data", bool)]
    )

    test_args = TestArgs("snazzy_new_benchmark", True)

    CreateBenchmarkPipelineCommand().make_benchmark_directories(
        root_path=tmpdir, benchmark_name=test_args.benchmark_name
    )

    for dataset_type in DatasetType:

        assert Path(
            tmpdir / "data" / test_args.benchmark_name / "datasets" / dataset_type.value
        ).exists
        assert Path(
            tmpdir
            / "test_data"
            / test_args.benchmark_name
            / "datasets"
            / dataset_type.value
        ).exists

    assert Path(
        tmpdir / "mcs_benchmark_data" / "pipelines" / test_args.benchmark_name
    ).exists()

    assert Path(
        tmpdir
        / "tests"
        / "mcs_benchmark_data_test"
        / "pipelines"
        / test_args.benchmark_name
    ).exists()

    CreateBenchmarkPipelineCommand().create_files_from_template(
        root_path=tmpdir,
        benchmark_name=test_args.benchmark_name,
        data_dir="TEST_DATA_DIR_PATH" if test_args.using_test_data else "DATA_DIR_PATH",
    )

    pipeline_path = Path(
        tmpdir
        / "mcs_benchmark_data/pipelines"
        / Path(test_args.benchmark_name)
        / f"{test_args.benchmark_name}_benchmark_pipeline.py"
    )

    assert pipeline_path.exists()

    with open(pipeline_path) as fp:
        assert fp.read().count(test_args.benchmark_name) == 3

    assert Path(
        tmpdir / "data" / Path(test_args.benchmark_name) / "metadata.json"
    ).exists()
