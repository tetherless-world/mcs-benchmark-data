from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)


def test_extract_transform():
    models = tuple(
        KagnetCommonsenseQaSubmissionPipeline(
            file_names=KagnetCommonsenseQaSubmissionFileNames(
                metadata="CommonsenseQA_dev_submissions.jsonl",
                submission_file_name="dev_rand_split_roberta_submission.jsonl",
            )
        ).extract_transform()
    )
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    assert submission.name == "CommonsenseQA-kagnet"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)
