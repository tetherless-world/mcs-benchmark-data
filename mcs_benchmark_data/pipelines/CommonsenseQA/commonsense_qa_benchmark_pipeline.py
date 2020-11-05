from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_extractor import (
    BenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.CommonsenseQA.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)
from mcs_benchmark_data.inline_labels_benchmark_file_names import (
    InlineLabelsBenchmarkFileNames,
)


class CommonsenseQaBenchmarkPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(self, file_names: InlineLabelsBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=CommonsenseQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaBenchmarkPipeline.main()