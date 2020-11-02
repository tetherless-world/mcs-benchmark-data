from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)

from tests.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        KagnetCommonsenseQaSubmissionPipeline(
            file_names=KagnetCommonsenseQaSubmissionFileNames(
                metadata="CommonsenseQA_dev_submissions.jsonl",
                submission="dev_rand_split_kagnet_submission.jsonl",
            )
        ).extract_transform()
    )
    assert_submission_models(
        KagnetCommonsenseQaSubmissionPipeline.ID,
        KagnetCommonsenseQaSubmissionPipeline.SUBMISSION_NAME,
        models,
    )
