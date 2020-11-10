from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded_test
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load():
    CommonsenseQaBenchmarkPipeline().extract_transform_load()
    assert_valid_rdf_loaded_test(CommonsenseQaBenchmarkPipeline.ID)
