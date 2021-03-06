from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_pipeline import (
    RobertaCommonsenseQaSubmissionPipeline,
)
from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform():
    RobertaCommonsenseQaSubmissionPipeline(
        data_dir_path=TEST_DATA_DIR_PATH,
    ).extract_transform_load()

    assert_valid_rdf_loaded(
        pipeline_id=RobertaCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        data_dir_path=TEST_DATA_DIR_PATH,
    )
