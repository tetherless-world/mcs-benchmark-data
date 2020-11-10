from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_pipeline import (
    Roberta4CycicSubmissionPipeline,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform():
    models = tuple(
        Roberta4CycicSubmissionPipeline(
            data_dir_path=TEST_DATA_DIR_PATH
        ).extract_transform()
    )
    assert_submission_models(
        benchmark_id=Roberta4CycicSubmissionPipeline.BENCHMARK_ID,
        submission_id=Roberta4CycicSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
