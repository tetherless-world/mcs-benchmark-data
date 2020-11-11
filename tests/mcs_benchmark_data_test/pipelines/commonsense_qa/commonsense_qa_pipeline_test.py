from mcs_benchmark_data.path import TEST_DATA_DIR_PATH
from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load():
    CommonsenseQaBenchmarkPipeline(
        data_dir_path=TEST_DATA_DIR_PATH
    ).extract_transform_load()
    assert_valid_rdf_loaded(
        pipeline_id=CommonsenseQaBenchmarkPipeline.ID, data_dir_path=TEST_DATA_DIR_PATH
    )
