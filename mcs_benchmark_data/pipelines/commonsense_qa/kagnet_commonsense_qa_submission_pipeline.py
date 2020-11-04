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
    BENCHMARK_ID = "CommonsenseQA"
    SUBMISSION_ID = "kagnet"

    def __init__(self, file_names: KagnetCommonsenseQaSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkSubmissionExtractor(
                pipeline_id=self.BENCHMARK_ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.BENCHMARK_ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                **kwds,
            ),
            **kwds,
        )


if __name__ == "__main__":
    KagnetCommonsenseQaSubmissionPipeline.main()
