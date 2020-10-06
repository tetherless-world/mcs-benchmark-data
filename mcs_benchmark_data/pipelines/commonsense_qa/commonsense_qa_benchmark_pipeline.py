from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_extractor import (
    CommonsenseQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)


class CommonsenseQaBenchmarkPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=CommonsenseQaBenchmarkExtractor(pipeline_id=self.ID, **kwds),
            id=self.ID,
            transformer=CommonsenseQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaBenchmarkPipeline.main()
