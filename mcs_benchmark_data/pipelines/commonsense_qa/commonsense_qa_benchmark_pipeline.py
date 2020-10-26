from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_extractor import (
    CommonsenseQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_file_names import (
    CommonsenseQaBenchmarkFileNames,
)


class CommonsenseQaBenchmarkPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(self, file_names: CommonsenseQaBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=CommonsenseQaBenchmarkExtractor(
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
