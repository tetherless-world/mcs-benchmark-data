import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from tests.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_file_names import (
    CommonsenseQaBenchmarkFileNames,
)


def test_extract_transform_load():
    CommonsenseQaBenchmarkPipeline(
        file_names=CommonsenseQaBenchmarkFileNames(
            metadata="metadata.json",
            train_samples="train_rand_split_small.jsonl",
            dev_samples="dev_rand_split_small.jsonl",
            test_samples="test_rand_split_no_answers_small.jsonl",
        ),
    ).extract_transform_load()
    assert_valid_rdf_loaded(CommonsenseQaBenchmarkPipeline.ID)
