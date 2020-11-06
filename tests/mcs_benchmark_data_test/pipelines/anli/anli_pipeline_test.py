from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.anli.anli_benchmark_pipeline import (
    AnliBenchmarkPipeline,
)
from mcs_benchmark_data.infile_labels_benchmark_file_names import (
    InfileLabelsBenchmarkFileNames,
)


def test_extract_transform_load():
    AnliBenchmarkPipeline(
        file_names=InfileLabelsBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="dev_labels.lst",
            dev_samples="dev_samples.jsonl",
            train_labels="train_labels.lst",
            train_samples="train_samples.jsonl",
            test_samples="test_samples.jsonl",
        ),
    ).extract_transform_load()
    assert_valid_rdf_loaded(AnliBenchmarkPipeline.ID)
