from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded


def test_extract_transform():
    KagnetCommonsenseQaSubmissionPipeline(
        data_dir_path=TEST_DATA_DIR_PATH,
    ).extract_transform_load()

    assert_valid_rdf_loaded(
        pipeline_id=KagnetCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        data_dir_path=TEST_DATA_DIR_PATH,
    )
