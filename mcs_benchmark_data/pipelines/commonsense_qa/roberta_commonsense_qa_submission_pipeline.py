from mcs_benchmark_data._submission_pipeline import _SubmissionPipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path

from mcs_benchmark_data.dataset_type import DatasetType

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.roberta_commonsense_qa_submission_transformer import (
    RobertaCommonsenseQaSubmissionTransformer,
)


class RobertaCommonsenseQaSubmissionPipeline(_SubmissionPipeline):
    BENCHMARK_ID = "commonsense_qa"
    SUBMISSION_ID = "roberta"

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
            transformer=RobertaCommonsenseQaSubmissionTransformer(
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
    RobertaCommonsenseQaSubmissionPipeline.main()
