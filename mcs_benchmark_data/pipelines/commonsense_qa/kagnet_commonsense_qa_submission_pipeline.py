from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_submission_extractor import (
    BenchmarkSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_transformer import (
    KagnetCommonsenseQaSubmissionTransformer,
)

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)


class KagnetCommonsenseQaSubmissionPipeline(_Pipeline):
    ID = "CommonsenseQA"
    SUBMISSION_NAME = "kagnet"

    def __init__(self, file_names: KagnetCommonsenseQaSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkSubmissionExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
                pipeline_id=self.ID, submission_name=self.SUBMISSION_NAME, **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    KagnetCommonsenseQaSubmissionPipeline.main()
