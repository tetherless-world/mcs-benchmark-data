from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_transformer import (
    RobertaCommonsenseQaSubmissionTransformer,
)


class RobertaCommonsenseQaSubmissionPipeline(_Pipeline):
    BENCHMARK_ID = "commonsense_qa"
    SUBMISSION_ID = "roberta"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=RobertaCommonsenseQaSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                data_dir_path=TEST_DATA_DIR_PATH,
                **kwds,
            ),
            **kwds,
        )


if __name__ == "__main__":
    RobertaCommonsenseQaSubmissionPipeline.main()
