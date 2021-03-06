from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)

from mcs_benchmark_data.path import TEST_DATA_DIR_PATH


def test_extract_transform():
    models = tuple(
        CommonsenseQaBenchmarkPipeline(
            data_dir_path=TEST_DATA_DIR_PATH
        ).extract_transform()
    )
    assert models

    benchmark = [model for model in models if isinstance(model, Benchmark)]
    assert benchmark
    benchmark = benchmark[0]
    assert benchmark.name == "CommonsenseQA"
    assert benchmark.authors[0] == "Alon Talmor"

    datasets = [model for model in models if isinstance(model, BenchmarkDataset)]
    assert len(datasets) == 3
    assert any(dataset.name == "CommonsenseQA dev dataset" for dataset in datasets)
    assert any(dataset.name == "CommonsenseQA test dataset" for dataset in datasets)
    assert any(dataset.name == "CommonsenseQA training dataset" for dataset in datasets)
