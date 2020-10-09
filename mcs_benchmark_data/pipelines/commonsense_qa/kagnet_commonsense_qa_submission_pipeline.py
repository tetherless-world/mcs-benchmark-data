from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_extractor import (
    KagnetCommonsenseQaSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_transformer import (
    KagnetCommonsenseQaSubmissionTransformer,
)


class KagnetCommonsenseQaSubmissionPipeline(_Pipeline):
    __ID = "CommonsenseQA"

    def __init__(
        self, submission_jsonl_file="dev_rand_split_kagnet_submission.jsonl", **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=KagnetCommonsenseQaSubmissionExtractor(
                pipeline_id=self.__ID,
                submission_jsonl_file=submission_jsonl_file,
                **kwds,
            ),
            id=self.__ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
                pipeline_id=self.__ID, **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    KagnetCommonsenseQaSubmissionPipeline.main()
