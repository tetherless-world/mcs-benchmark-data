from mcs_benchmark_data._submission_pipeline import _SubmissionPipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path
from mcs_benchmark_data.dataset_type import DatasetType

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.loaders.rdf_file_loader import RdfFileLoader
from mcs_benchmark_data.pipelines.benchmark_name.submission_name_benchmark_name_submission_transformer import (
    SubmissionNameBenchmarkNameSubmissionTransformer,
)


class SubmissionNameBenchmarkNameSubmissionPipeline(_SubmissionPipeline):
    BENCHMARK_ID = "benchmark_name"
    SUBMISSION_ID = "submission_name"

    def __init__(
        self,
        *,
        data_dir_path: Path = DATA_DIR_PATH,
        dataset_type: DatasetType = _SubmissionPipeline.DATASET_TYPE_DEFAULT,
        **kwds,
    ):
        _SubmissionPipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=SubmissionNameBenchmarkNameSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                data_dir_path=data_dir_path,
                dataset_type=getattr(DatasetType, dataset_type.upper()).value,
                **kwds,
            ),
            loader=RdfFileLoader(
                pipeline_id=self.BENCHMARK_ID,
                data_dir_path=data_dir_path,
                file_path=self._loaded_file_path(
                    data_dir_path=data_dir_path,
                    submission_id=self.SUBMISSION_ID,
                    benchmark_id=self.BENCHMARK_ID,
                ),
                **kwds,
            ),
            data_dir_path=data_dir_path,
            **kwds,
        )


if __name__ == "__main__":
    SubmissionNameBenchmarkNameSubmissionPipeline.main()
