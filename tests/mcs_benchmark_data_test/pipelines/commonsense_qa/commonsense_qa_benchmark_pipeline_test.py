from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform():
    models = tuple(CommonsenseQaBenchmarkPipeline().extract_transform())
    assert models
    assert len(models) == 4

    assert type(list(models[0])) == "Benchmark"

    benchmark = [model for model in models if isinstance(model, Benchmark)]
    assert benchmark
    benchmark = benchmark[0]
    assert benchmark.name == "CommonsenseQA"

    datasets = [model for model in models if isinstance(model, BenchmarkDataset)]
    assert len(datasets) == 3
    assert any(dataset.name == "dev" for dataset in datasets)
    assert any(dataset.name == "test" for dataset in datasets)
    assert any(dataset.name == "train" for dataset in datasets)
