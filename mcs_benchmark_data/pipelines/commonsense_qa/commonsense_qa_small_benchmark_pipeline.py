from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_small_benchmark_extractor import (
    CommonsenseQaSmallBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)


class CommonsenseQaSmallBenchmarkPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=CommonsenseQaSmallBenchmarkExtractor(pipeline_id=self.ID, **kwds),
            id=self.ID,
            transformer=CommonsenseQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaSmallBenchmarkPipeline.main()
