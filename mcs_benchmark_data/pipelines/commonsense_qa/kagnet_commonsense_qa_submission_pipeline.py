from mcs_benchmark_data._submission_pipeline import _SubmissionPipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path
from mcs_benchmark_data.dataset_type import DatasetType

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_transformer import (
    KagnetCommonsenseQaSubmissionTransformer,
)


class KagnetCommonsenseQaSubmissionPipeline(_SubmissionPipeline):
    BENCHMARK_ID = "commonsense_qa"
    SUBMISSION_ID = "kagnet"

    def __init__(
        self,
        *,
        data_dir_path: Path = DATA_DIR_PATH,
        dataset_type: DatasetType = _SubmissionPipeline.DATASET_TYPE_DEFAULT,
        **kwds
    ):
        _SubmissionPipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=KagnetCommonsenseQaSubmissionTransformer(
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
    KagnetCommonsenseQaSubmissionPipeline.main()
