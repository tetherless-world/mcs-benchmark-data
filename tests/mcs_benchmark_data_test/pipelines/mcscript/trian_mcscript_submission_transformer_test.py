from mcs_benchmark_data.pipelines.MCScript.trian_mcscript_submission_pipeline import (
    TrianMCScriptSubmissionPipeline,
)
from mcs_benchmark_data.pipelines.MCScript.trian_mcscript_submission_file_names import (
    TrianMCScriptSubmissionFileNames,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models


def test_extract_transform():
    models = tuple(
        TrianMCScriptSubmissionPipeline(
            file_names=TrianMCScriptSubmissionFileNames(
                metadata="submissions_metadata.json",
                submission="trian_dev_submission.txt",
            )
        ).extract_transform()
    )

    assert_submission_models(
        benchmark_id=TrianMCScriptSubmissionPipeline.BENCHMARK_ID,
        submission_id=TrianMCScriptSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
