from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_extractor import (
    BenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_transformer import (
    PhysicalIQaBenchmarkTransformer,
)
from mcs_benchmark_data.infile_labels_benchmark_file_names import (
    InfileLabelsBenchmarkFileNames,
)


class PhysicalIQaBenchmarkPipeline(_Pipeline):
    ID = "physical_iqa"

    def __init__(self, file_names: InfileLabelsBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkExtractor(
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
