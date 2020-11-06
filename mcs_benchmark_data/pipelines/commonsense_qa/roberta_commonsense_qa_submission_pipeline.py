from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_submission_extractor import (
    BenchmarkSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_transformer import (
    RobertaCommonsenseQaSubmissionTransformer,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_file_names import (
    RobertaCommonsenseQaSubmissionFileNames,
)


class RobertaCommonsenseQaSubmissionPipeline(_Pipeline):
    BENCHMARK_ID = "commonsense_qa"
    SUBMISSION_ID = "roberta"

    def __init__(self, file_names: RobertaCommonsenseQaSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkSubmissionExtractor(
                pipeline_id=self.BENCHMARK_ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.BENCHMARK_ID,
            transformer=RobertaCommonsenseQaSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                **kwds,
            ),
            **kwds,
        )


if __name__ == "__main__":
    RobertaCommonsenseQaSubmissionPipeline.main()
