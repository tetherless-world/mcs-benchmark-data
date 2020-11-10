from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded_test
from mcs_benchmark_data.pipelines.anli.anli_benchmark_pipeline import (
    AnliBenchmarkPipeline,
)


def test_extract_transform_load():
    AnliBenchmarkPipeline().extract_transform_load()
    assert_valid_rdf_loaded_test(AnliBenchmarkPipeline.ID)
