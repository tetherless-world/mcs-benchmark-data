from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_pipeline import (
    TrianMCScriptSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_file_names import (
    TrianMCScriptSubmissionFileNames,
)

from tests.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        TrianMCScriptSubmissionPipeline(
            file_names=TrianMCScriptSubmissionFileNames(
                metadata="MCScript_dev_submissions.jsonl",
                submission="trian_dev_submission.jsonl",
            )
        ).extract_transform()
    )
    assert_submission_models(
        TrianMCScriptSubmissionPipeline.ID,
        TrianMCScriptSubmissionPipeline.SUBMISSION_NAME,
        models,
    )
