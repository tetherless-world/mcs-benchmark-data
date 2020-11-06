from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
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
            dev_samples="dev_samples.xml",
            train_samples="train_samples.xml",
            test_samples="test_samples.xml",
        ),
    ).extract_transform_load()

    assert_valid_rdf_loaded(MCScriptBenchmarkPipeline.ID)
