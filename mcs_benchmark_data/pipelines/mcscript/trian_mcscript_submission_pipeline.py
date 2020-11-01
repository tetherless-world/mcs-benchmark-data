from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_submission_extractor import (
    BenchmarkSubmissionExtractor,
)
from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_transformer import (
    TrianMCScriptSubmissionTransformer,
)

from mcs_benchmark_data.pipelines.mcscript.trian_mcscript_submission_file_names import (
    TrianMCScriptSubmissionFileNames,
)


class TrianMCScriptSubmissionPipeline(_Pipeline):
    __ID = "MCScript"

    def __init__(self, file_names: TrianMCScriptSubmissionFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkSubmissionExtractor(
                pipeline_id=self.__ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.__ID,
            transformer=TrianMCScriptSubmissionTransformer(
                pipeline_id=self.__ID, submission_name="trian", **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    TrianMCScriptSubmissionPipeline.main()
