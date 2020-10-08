from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_small_submission_extractor import (
    KagnetCommonsenseQaSmallSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_transformer import (
    KagnetCommonsenseQaSubmissionTransformer,
)


class KagnetCommonsenseQaSmallSubmissionPipeline(_Pipeline):
    __ID = "CommonsenseQA"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=KagnetCommonsenseQaSmallSubmissionExtractor(
                pipeline_id=self.__ID, **kwds
            ),
            id=self.__ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
                pipeline_id=self.__ID, **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    KagnetCommonsenseQaSmallSubmissionPipeline.main()
