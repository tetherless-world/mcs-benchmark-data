from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_pipeline import (
    Roberta4CycicSubmissionPipeline,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(Roberta4CycicSubmissionPipeline().extract_transform())
    assert_submission_models(
        benchmark_id=Roberta4CycicSubmissionPipeline.BENCHMARK_ID,
        submission_id=Roberta4CycicSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
