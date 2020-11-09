import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load():
    CommonsenseQaBenchmarkPipeline().extract_transform_load()
    assert_valid_rdf_loaded(CommonsenseQaBenchmarkPipeline.ID)
