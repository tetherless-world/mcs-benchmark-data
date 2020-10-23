import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_pipeline import (
    PhysicalIQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_file_names import (
    PhysicalIQaBenchmarkFileNames,
)


def test_extract_transform_load():
    PhysicalIQaBenchmarkPipeline(
        file_names=PhysicalIQaBenchmarkFileNames(
            meta_data="metadata.json",
            dev_labels="dev-labels.lst",
            dev_samples="dev.jsonl",
            train_labels="train-labels.lst",
            train_samples="train.jsonl",
            test_samples="test.jsonl",
        ),
    ).extract_transform_load()

    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / PhysicalIQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (
        PhysicalIQaBenchmarkPipeline.ID + ".turtle.bz2"
    )
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="turtle")
