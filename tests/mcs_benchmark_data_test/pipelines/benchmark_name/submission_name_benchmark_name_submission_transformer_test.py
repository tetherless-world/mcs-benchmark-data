from mcs_benchmark_data.pipelines.benchmark_name.submission_name_benchmark_name_submission_pipeline import (
    SubmissionNameBenchmarkNameSubmissionPipeline,
)

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded


def test_extract_transform():
    SubmissionNameBenchmarkNameSubmissionPipeline(
        data_dir_path=TEST_DATA_DIR_PATH,
    ).extract_transform_load()

    assert_valid_rdf_loaded(
        pipeline_id=SubmissionNameBenchmarkNameSubmissionPipeline.BENCHMARK_ID,
        data_dir_path=TEST_DATA_DIR_PATH,
    )
