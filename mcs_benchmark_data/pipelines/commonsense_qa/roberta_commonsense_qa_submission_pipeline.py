from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_extractor import (
    RobertaCommonsenseQaSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_transformer import (
    RobertaCommonsenseQaSubmissionTransformer,
)


class RobertaCommonsenseQaSubmissionPipeline(_Pipeline):
    __ID = "CommonsenseQA"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=RobertaCommonsenseQaSubmissionExtractor(
                pipeline_id=self.__ID, **kwds
            ),
            id=self.__ID,
            transformer=RobertaCommonsenseQaSubmissionTransformer(
                pipeline_id=self.__ID, system="Roberta", **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    RobertaCommonsenseQaSubmissionPipeline.main()
