from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded_test
from mcs_benchmark_data.pipelines.cycic.cycic_benchmark_pipeline import (
    CycicBenchmarkPipeline,
)


def test_extract_transform_load():
    CycicBenchmarkPipeline().extract_transform_load()

    assert_valid_rdf_loaded_test(CycicBenchmarkPipeline.ID)
