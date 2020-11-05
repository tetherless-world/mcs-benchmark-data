from tests.mcs_benchmark_data_test.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.cycic.cycic_benchmark_pipeline import (
    CycicBenchmarkPipeline,
)
from mcs_benchmark_data.infile_labels_benchmark_file_names import (
    InfileLabelsBenchmarkFileNames,
)


def test_extract_transform_load():
    CycicBenchmarkPipeline(
        file_names=InfileLabelsBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="CycIC_dev_labels_small.jsonl",
            dev_samples="CycIC_dev_questions_small.jsonl",
            train_labels="CycIC_training_labels_small.jsonl",
            train_samples="CycIC_training_questions_small.jsonl",
            test_samples=None,
        ),
    ).extract_transform_load()

    assert_valid_rdf_loaded(CycicBenchmarkPipeline.ID)
