from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_pipeline import (
    MCScriptBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_file_names import (
    MCScriptBenchmarkFileNames,
)


def test_extract_transform():
    models = tuple(
        MCScriptBenchmarkPipeline(
            file_names=MCScriptBenchmarkFileNames(
                metadata="metadata.json",
                dev_samples="dev-data.xml",
                train_samples="train-data.xml",
                test_samples="test-data.xml",
            ),
        ).extract_transform()
    )
    assert models

    benchmark = [model for model in models if isinstance(model, Benchmark)]
    assert benchmark
    benchmark = benchmark[0]
    assert benchmark.name == "MCScript"
    assert benchmark.authors[0] == "Simon Ostermann"

    datasets = [model for model in models if isinstance(model, BenchmarkDataset)]
    assert len(datasets) == 3
    assert any(dataset.name == "MCScript dev dataset" for dataset in datasets)
    assert any(dataset.name == "MCScript test dataset" for dataset in datasets)
    assert any(dataset.name == "MCScript training dataset" for dataset in datasets)
