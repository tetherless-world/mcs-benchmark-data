from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import DATA_DIR_PATH
from pathlib import Path

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_transformer import (
    TrianMCScriptSubmissionTransformer,
)


class TrianMCScriptSubmissionPipeline(_Pipeline):
    BENCHMARK_ID = "mcscript"
    SUBMISSION_ID = "trian"

    def __init__(self, data_dir_path: Path = DATA_DIR_PATH, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.BENCHMARK_ID),
            id=self.BENCHMARK_ID,
            transformer=TrianMCScriptSubmissionTransformer(
                pipeline_id=self.BENCHMARK_ID,
                submission_id=self.SUBMISSION_ID,
                data_dir_path=data_dir_path,
                **kwds,
            ),
            data_dir_path=data_dir_path,
            **kwds,
        )


if __name__ == "__main__":
    TrianMCScriptSubmissionPipeline.main()
