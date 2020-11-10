from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded_test
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_pipeline import (
    PhysicalIQaBenchmarkPipeline,
)


def test_extract_transform_load():
    PhysicalIQaBenchmarkPipeline().extract_transform_load()

    assert_valid_rdf_loaded_test(PhysicalIQaBenchmarkPipeline.ID)
