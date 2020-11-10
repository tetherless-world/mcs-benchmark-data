from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_transformer import (
    MCScriptBenchmarkTransformer,
)


class MCScriptBenchmarkPipeline(_Pipeline):
    ID = "mcscript"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.ID),
            id=self.ID,
            transformer=MCScriptBenchmarkTransformer(
                pipeline_id=self.ID, data_dir_path=TEST_DATA_DIR_PATH, **kwds
            ),
            data_dir_path=TEST_DATA_DIR_PATH,
            **kwds,
        )


if __name__ == "__main__":
    MCScriptBenchmarkPipeline.main()
