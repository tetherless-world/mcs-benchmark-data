from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        KagnetCommonsenseQaSubmissionPipeline(
            file_names=KagnetCommonsenseQaSubmissionFileNames(
                metadata="submissions_metadata.jsonl",
                submission="kagnet_dev_submission.jsonl",
            )
        ).extract_transform()
    )
    assert_submission_models(
        benchmark_id=KagnetCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        submission_id=KagnetCommonsenseQaSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
