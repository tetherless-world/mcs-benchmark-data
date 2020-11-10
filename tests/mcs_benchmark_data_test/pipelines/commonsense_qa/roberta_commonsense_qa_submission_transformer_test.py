from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_pipeline import (
    RobertaCommonsenseQaSubmissionPipeline,
)
from tests.mcs_benchmark_data_test.assertions import assert_submission_models

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform():
    models = tuple(
        RobertaCommonsenseQaSubmissionPipeline(
            data_dir_path=TEST_DATA_DIR_PATH
        ).extract_transform()
    )
    assert_submission_models(
        benchmark_id=RobertaCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        submission_id=RobertaCommonsenseQaSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
