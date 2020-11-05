from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_pipeline import (
    RobertaCommonsenseQaSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_file_names import (
    RobertaCommonsenseQaSubmissionFileNames,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        RobertaCommonsenseQaSubmissionPipeline(
            file_names=RobertaCommonsenseQaSubmissionFileNames(
                metadata="submissions_metadata.json",
                submission="dev_rand_split_roberta_submission_small.jsonl",
            )
        ).extract_transform_load()
    )
    assert_submission_models(
        benchmark_id=RobertaCommonsenseQaSubmissionPipeline.BENCHMARK_ID,
        submission_id=RobertaCommonsenseQaSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
