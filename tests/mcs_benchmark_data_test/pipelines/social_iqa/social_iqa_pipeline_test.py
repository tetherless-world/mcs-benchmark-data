import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_pipeline import (
    SocialIQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_file_names import (
    SocialIQaBenchmarkFileNames,
)


def test_extract_transform_load():
    SocialIQaBenchmarkPipeline(
        file_names=SocialIQaBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="dev-labels.lst",
            dev_samples="dev.jsonl",
            train_labels="train-labels.lst",
            train_samples="train.jsonl",
        ),
    ).extract_transform_load()

    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / SocialIQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (
        SocialIQaBenchmarkPipeline.ID + ".ttl.bz2"
    )
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="ttl")
