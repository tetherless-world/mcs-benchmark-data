from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_extractor import (
    MCScriptBenchmarkExtractor,
)


def test_extract():
    MCScriptBenchmarkExtractor(
        dev_xml_file_name="dev-data.xml",
        test_xml_file_name="test-data.xml",
        train_xml_file_name="train-data.xml",
    ).extract()
