import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_file_names import (
    CommonsenseQaBenchmarkFileNames,
)


def test_extract_transform_load(tmp_path):
    CommonsenseQaBenchmarkPipeline(
        file_names=CommonsenseQaBenchmarkFileNames(
            meta_data="metadata.json",
            train_samples="train_rand_split_small.jsonl",
            dev_samples="dev_rand_split_small.jsonl",
            test_samples="test_rand_split_no_answers_small.jsonl",
        ),
    ).extract_transform_load()
    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / CommonsenseQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (
        CommonsenseQaBenchmarkPipeline.ID + ".turtle.bz2"
    )
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="turtle")
