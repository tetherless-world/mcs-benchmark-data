from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_transformer import (
    PhysicalIQaBenchmarkTransformer,
)


class PhysicalIQaBenchmarkPipeline(_Pipeline):
    ID = "physical_iqa"

    def __init__(self, data_dir_path: Path = DATA_DIR_PATH, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.ID),
            id=self.ID,
            transformer=PhysicalIQaBenchmarkTransformer(
                pipeline_id=self.ID, data_dir_path=data_dir_path, **kwds
            ),
            data_dir_path=data_dir_path,
            **kwds,
        )


if __name__ == "__main__":
    PhysicalIQaBenchmarkPipeline.main()
