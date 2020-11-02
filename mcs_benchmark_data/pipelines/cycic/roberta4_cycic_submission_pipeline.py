from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_submission_extractor import (
    BenchmarkSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_transformer import (
    Roberta4CycicSubmissionTransformer,
)

from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_file_names import (
    Roberta4CycicSubmissionFileNames,
)


class Roberta4CycicSubmissionPipeline(_Pipeline):
    ID = "CycIC"
    SUBMISSION_NAME = "roberta4"

    def __init__(self, file_names: Roberta4CycicSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkSubmissionExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=Roberta4CycicSubmissionTransformer(
                pipeline_id=self.ID, submission_name=self.SUBMISSION_NAME, **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    Roberta4CycicSubmissionPipeline.main()
