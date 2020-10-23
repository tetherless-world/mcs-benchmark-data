from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_extractor import (
    MCScriptBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_transformer import (
    MCScriptBenchmarkTransformer,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_file_names import (
    MCScriptBenchmarkFileNames,
)


class MCScriptBenchmarkPipeline(_Pipeline):
    ID = "MCScript"

    def __init__(self, file_names: MCScriptBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=MCScriptBenchmarkExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=MCScriptBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    MCScriptBenchmarkPipeline.main()