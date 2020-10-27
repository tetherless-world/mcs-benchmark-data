import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.cycic.cycic_benchmark_pipeline import (
    CycicBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.cycic.cycic_benchmark_file_names import (
    CycicBenchmarkFileNames,
)


def test_extract_transform_load():
    CycicBenchmarkPipeline(
        file_names=CycicBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="CycIC_dev_labels.jsonl",
            dev_samples="CycIC_dev_questions.jsonl",
            train_labels="CycIC_training_labels.jsonl",
            train_samples="CycIC_training_questions.jsonl",
        ),
    ).extract_transform_load()

    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / CycicBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (CycicBenchmarkPipeline.ID + ".ttl.bz2")
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="ttl")
