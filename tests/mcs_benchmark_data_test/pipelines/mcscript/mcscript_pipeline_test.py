from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded_test
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_pipeline import (
    MCScriptBenchmarkPipeline,
)


def test_extract_transform_load():
    MCScriptBenchmarkPipeline().extract_transform_load()

    assert_valid_rdf_loaded_test(MCScriptBenchmarkPipeline.ID)
