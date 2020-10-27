from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_extractor import (
    BenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_transformer import (
    Roberta4CycicSubmissionTransformer,
)

from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_file_names import (
    Roberta4CycicSubmissionFileNames,
)


class Roberta4CycicSubmissionPipeline(_Pipeline):
    __ID = "Roberta4CycIC"

    def __init__(self, file_names: Roberta4CycicSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkExtractor(
                pipeline_id=self.__ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.__ID,
            transformer=Roberta4CycicSubmissionTransformer(
                pipeline_id=self.__ID, system="Roberta4", **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    Roberta4CycicSubmissionPipeline.main()
