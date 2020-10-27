from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_file_names import (
    CommonsenseQaBenchmarkFileNames,
)


def test_extract_transform():
    models = tuple(
        CommonsenseQaBenchmarkPipeline(
            file_names=CommonsenseQaBenchmarkFileNames(
                metadata="metadata.json",
                train_samples="train_rand_split_small.jsonl",
                dev_samples="dev_rand_split_small.jsonl",
                test_samples="test_rand_split_no_answers_small.jsonl",
            ),
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
