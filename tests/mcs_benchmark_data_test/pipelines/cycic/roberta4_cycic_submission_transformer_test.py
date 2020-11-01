from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_pipeline import (
    Roberta4CycicSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_file_names import (
    Roberta4CycicSubmissionFileNames,
)


def test_extract_transform():
    models = tuple(
        Roberta4CycicSubmissionPipeline(
            file_names=Roberta4CycicSubmissionFileNames(
                metadata="CycIC_dev_submissions.jsonl",
                submission="CycIC_dev_cycic-transformers_submission.jsonl",
            )
        ).extract_transform()
    )
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    assert submission.name == "cycic-roberta4"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)
