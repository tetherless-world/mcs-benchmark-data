from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_pipeline import (
    TrianMCScriptSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_file_names import (
    TrianMCScriptSubmissionFileNames,
)


def test_extract_transform():
    models = tuple(
        TrianMCScriptSubmissionPipeline(
            file_names=TrianMCScriptSubmissionFileNames(
                metadata="MCScript_dev_submissions.jsonl",
                submission="trian_dev_submission.jsonl",
            )
        ).extract_transform()
    )
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    assert submission.name == "MCScript-trian"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)
