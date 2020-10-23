from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_extractor import (
    PhysicalIQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_transformer import (
    PhysicalIQaBenchmarkTransformer,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_file_names import (
    PhysicalIQaBenchmarkFileNames,
)


class PhysicalIQaBenchmarkPipeline(_Pipeline):
    ID = "PhysicalIQa"

    def __init__(self, file_names=PhysicalIQaBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=PhysicalIQaBenchmarkExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=PhysicalIQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    PhysicalIQaBenchmarkPipeline.main()