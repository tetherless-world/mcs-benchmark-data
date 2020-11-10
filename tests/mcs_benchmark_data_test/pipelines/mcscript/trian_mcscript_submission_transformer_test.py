from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_pipeline import (
    TrianMCScriptSubmissionPipeline,
)

from tests.mcs_benchmark_data_test.assertions import assert_submission_models

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform():
    models = tuple(
        TrianMCScriptSubmissionPipeline(
            data_dir_path=TEST_DATA_DIR_PATH
        ).extract_transform()
    )

    assert_submission_models(
        benchmark_id=TrianMCScriptSubmissionPipeline.BENCHMARK_ID,
        submission_id=TrianMCScriptSubmissionPipeline.SUBMISSION_ID,
        models=models,
    )
