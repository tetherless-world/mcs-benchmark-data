from mcs_benchmark_data._submission_pipeline import _SubmissionPipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path
from mcs_benchmark_data.dataset_type import DatasetType

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_transformer import (
    Roberta4CycicSubmissionTransformer,
)


class Roberta4CycicSubmissionPipeline(_SubmissionPipeline):
    BENCHMARK_ID = "cycic"
    SUBMISSION_ID = "roberta4"

    def __init__(
        self,
        *,
        data_dir_path: Path = DATA_DIR_PATH,
        dataset_type: str = _SubmissionPipeline.DATASET_TYPE_DEFAULT,
        **kwds
    ):
        _SubmissionPipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=Roberta4CycicSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                data_dir_path=data_dir_path,
                dataset_type=getattr(DatasetType, dataset_type.upper()).value,
                **kwds,
            ),
            data_dir_path=data_dir_path,
            **kwds,
        )


if __name__ == "__main__":
    Roberta4CycicSubmissionPipeline.main()
