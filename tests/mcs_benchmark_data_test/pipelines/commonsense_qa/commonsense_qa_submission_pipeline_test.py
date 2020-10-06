from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_pipeline import (
    KagnetCommonsenseQaSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_pipeline import (
    RobertaCommonsenseQaSubmissionPipeline,
)


def test_extract_transform_kagnet_submission_benchmark():
    models = tuple(KagnetCommonsenseQaSubmissionPipeline().extract_transform())
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    assert submission.name == "CommonsenseQA-kagnet"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)


def test_extract_transform_roberta_submission_benchmark():
    models = tuple(RobertaCommonsenseQaSubmissionPipeline().extract_transform())
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    assert submission.name == "CommonsenseQA-roberta"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)
