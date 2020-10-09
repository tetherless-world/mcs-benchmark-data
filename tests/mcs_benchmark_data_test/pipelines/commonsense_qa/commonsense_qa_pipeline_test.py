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

    # with open(rdf_file_path) as loaded_rdf:
    #     rdf_lines = list(loaded_rdf)

    # test_resource = rdf_lines[1]

    # assert test_resource == "BenchmarkSample"
    # assert test_resource["@type"] == "BenchmarkSample"
    # assert test_resource["antecedent"] == "BenchmarkSample"

    # old_graph = Graph()
    # for suffix in ("dev", "test", "train"):
    #     with open(
    #         loaded_data_dir_path
    #         / f"{CommonsenseQaBenchmarkPipeline.ID}_{suffix}.jsonl",
    #         "rb",
    #     ) as jsonl_file:
    #         for json_line in jsonl_file:
    #             if not json_line.strip():
    #                 continue
    #             old_graph.parse(source=StringInputSource(json_line), format="json-ld")

    new_graph = Graph()
    with open(rdf_file_path) as jsonl_file:
        # for json_line in jsonl_file:
        #     if not json_line.strip():
        #         continue
        new_graph.parse(data=jsonl_file.read(), format="json-ld")

    # old_graph = to_isomorphic(old_graph)
    # new_graph = to_isomorphic(new_graph)

    # See dump examples in https://rdflib.readthedocs.io/en/4.0/_modules/rdflib/compare.html
    # assert new_graph == old_graph

    # More likely pick out a few resources and compare them