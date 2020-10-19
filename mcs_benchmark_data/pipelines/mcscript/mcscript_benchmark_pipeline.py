from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_extractor import (
    MCScriptBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_transformer import (
    MCScriptBenchmarkTransformer,
)


class MCScriptBenchmarkPipeline(_Pipeline):
    ID = "MCScript"

    def __init__(
        self,
        dev_json_file_name="dev-data.json",
        test_json_file_name="test-data.json",
        train_json_file_name="train-data.json",
        **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=MCScriptBenchmarkExtractor(
                pipeline_id=self.ID,
                dev_file_name=dev_json_file_name,
                test_file_name=test_json_file_name,
                train_file_name=train_json_file_name,
                **kwds,
            ),
            id=self.ID,
            transformer=MCScriptBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    MCScriptBenchmarkPipeline.main()
