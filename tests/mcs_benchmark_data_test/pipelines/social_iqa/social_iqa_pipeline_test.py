from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_pipeline import (
    SocialIQaBenchmarkPipeline,
)


def test_extract_transform_load():
    SocialIQaBenchmarkPipeline().extract_transform_load()

    assert_valid_rdf_loaded(SocialIQaBenchmarkPipeline.ID)
