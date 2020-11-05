from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.ANLI.anli_benchmark_pipeline import (
    AnliBenchmarkPipeline,
)
from mcs_benchmark_data.infile_labels_benchmark_file_names import (
    InfileLabelsBenchmarkFileNames,
)


def test_extract_transform_load():
    AnliBenchmarkPipeline(
        file_names=InfileLabelsBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="dev-labels_small.lst",
            dev_samples="dev_small.jsonl",
            train_labels="train-labels_small.lst",
            train_samples="train_small.jsonl",
            test_samples="test_small.jsonl",
        ),
    ).extract_transform_load()
    assert_valid_rdf_loaded(AnliBenchmarkPipeline.ID)
