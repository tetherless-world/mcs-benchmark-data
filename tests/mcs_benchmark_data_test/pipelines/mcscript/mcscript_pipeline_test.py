import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from tests.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_pipeline import (
    MCScriptBenchmarkPipeline,
)
from mcs_benchmark_data.inline_labels_benchmark_file_names import (
    InlineLabelsBenchmarkFileNames,
)


def test_extract_transform_load():
    MCScriptBenchmarkPipeline(
        file_names=InlineLabelsBenchmarkFileNames(
            metadata="metadata.json",
            dev_samples="dev-data_small.xml",
            train_samples="train-data_small.xml",
            test_samples="test-data_small.xml",
        ),
    ).extract_transform_load()

    assert_valid_rdf_loaded(MCScriptBenchmarkPipeline.ID)
