from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from tests.mcs_benchmark_data_test.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        KagnetCommonsenseQaSubmissionPipeline(
            data_dir_path=TEST_DATA_DIR_PATH
        ).extract_transform()
    )
    assert_submission_models(
        benchmark_id=KagnetCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        submission_id=KagnetCommonsenseQaSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
