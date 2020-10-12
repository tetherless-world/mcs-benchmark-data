from io import StringIO

from rdflib import Graph
from rdflib.compare import to_isomorphic
from rdflib.parser import StringInputSource

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load(tmp_path):
    CommonsenseQaBenchmarkPipeline(
        dev_jsonl_file="dev_rand_split_small.jsonl",
        test_jsonl_file="test_rand_split_no_answers_small.jsonl",
        train_jsonl_file="train_rand_split_small.jsonl",
    ).extract_transform_load()
    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / CommonsenseQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_file_path = loaded_data_dir_path / (
        CommonsenseQaBenchmarkPipeline.ID + ".jsonld"
    )
    assert rdf_file_path.is_file()

    new_graph = Graph()
    with open(rdf_file_path) as jsonl_file:

        new_graph.parse(data=jsonl_file.read(), format="json-ld")
