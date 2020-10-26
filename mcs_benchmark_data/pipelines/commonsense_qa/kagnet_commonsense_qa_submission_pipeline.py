from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_extractor import (
    KagnetCommonsenseQaSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_transformer import (
    KagnetCommonsenseQaSubmissionTransformer,
)

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)


class KagnetCommonsenseQaSubmissionPipeline(_Pipeline):
    __ID = "CommonsenseQA"

    def __init__(self, file_names: KagnetCommonsenseQaSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=KagnetCommonsenseQaSubmissionExtractor(
                pipeline_id=self.__ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.__ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
                pipeline_id=self.__ID, system="Kagnet", **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    KagnetCommonsenseQaSubmissionPipeline.main()
