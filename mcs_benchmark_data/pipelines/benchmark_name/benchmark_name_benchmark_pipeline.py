from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import DATA_DIR_PATH

from pathlib import Path

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.benchmark_name.benchmark_name_benchmark_transformer import (
    BenchmarkNameBenchmarkTransformer,
)


class BenchmarkNameBenchmarkPipeline(_Pipeline):
    ID = "benchmark_name"

    def __init__(self, *, data_dir_path: Path = DATA_DIR_PATH, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.ID, **kwds),
            id=self.ID,
            transformer=BenchmarkNameBenchmarkTransformer(
                pipeline_id=self.ID, data_dir_path=data_dir_path, **kwds
            ),
            data_dir_path=data_dir_path,
            **kwds,
        )


if __name__ == "__main__":
    BenchmarkNameBenchmarkPipeline.main()
