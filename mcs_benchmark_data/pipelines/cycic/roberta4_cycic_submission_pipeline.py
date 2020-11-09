from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_transformer import (
    Roberta4CycicSubmissionTransformer,
)


class Roberta4CycicSubmissionPipeline(_Pipeline):
    BENCHMARK_ID = "cycic"
    SUBMISSION_ID = "roberta4"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=Roberta4CycicSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                data_dir_path=TEST_DATA_DIR_PATH,
                **kwds,
            ),
            **kwds,
        )


if __name__ == "__main__":
    Roberta4CycicSubmissionPipeline.main()
