from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_pipeline import (
    PhysicalIQaBenchmarkPipeline,
)

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform_load():
    PhysicalIQaBenchmarkPipeline(
        data_dir_path=TEST_DATA_DIR_PATH
    ).extract_transform_load()

    assert_valid_rdf_loaded(
        pipeline_id=PhysicalIQaBenchmarkPipeline.ID, data_dir_path=TEST_DATA_DIR_PATH
    )
