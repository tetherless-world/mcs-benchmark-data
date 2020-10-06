from rdflib import Graph
from rdflib.compare import to_isomorphic

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load(tmp_path):
    CommonsenseQaBenchmarkPipeline().extract_transform_load()
    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / CommonsenseQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_file_path = loaded_data_dir_path / (CommonsenseQaBenchmarkPipeline.ID + ".ttl")
    assert rdf_file_path.is_file()

    old_graph = Graph()
    for suffix in ("dev", "test", "train"):
        with open(
            loaded_data_dir_path / f"{CommonsenseQaBenchmarkPipeline.ID}_{suffix}.jsonl"
        ) as jsonl_file:
            for json_line in jsonl_file:
                old_graph.parse(data=json_line, format="json-ld")

    new_graph = Graph()
    new_graph.parse(
        str(loaded_data_dir_path / f"{CommonsenseQaBenchmarkPipeline.ID}.ttl")
    )

    old_graph = to_isomorphic(old_graph)
    new_graph = to_isomorphic(new_graph)

    # See dump examples in https://rdflib.readthedocs.io/en/4.0/_modules/rdflib/compare.html
    assert new_graph == old_graph

    # More likely pick out a few resources and compare them
