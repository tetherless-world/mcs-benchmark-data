from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_extractor import (
    CommonsenseQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_submissoin_transformer import (
    CommonsenseQaSubmissionTransformer,
)


class CommonsenseQaRobertaSubmissionPipeline(_Pipeline):
    __ID = "CommonsenseQA"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=CommonsenseQaBenchmarkExtractor(pipeline_id=self.__ID, **kwds),
            id=self.__ID,
            transformer=CommonsenseQaSubmissionTransformer(
                pipeline_id=self.__ID, system="Roberta", **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaRobertaSubmissionPipeline.main()

