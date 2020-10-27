import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from tests.assertions import assert_valid_rdf_loaded
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

    assert_valid_rdf_loaded(CycicBenchmarkPipeline.ID)
