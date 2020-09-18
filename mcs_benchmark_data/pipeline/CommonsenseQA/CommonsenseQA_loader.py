from mcs-benchmark-data.loader.composite_loader import CompositeLoader
from mcs-benchmark-data.loader.json.jsonl_benchmark_answer_loader import (
    JsonlBenchmarkAnswerLoader,
)
from mcs-benchmark-data.loader.json.jsonl_benchmark_loader import JsonlBenchmarkLoader
from mcs-benchmark-data.loader.json.jsonl_benchmark_question_loader import (
    JsonlBenchmarkQuestionLoader,
)
from mcs-benchmark-data.loader.json.jsonl_benchmark_submission_loader import (
    JsonlBenchmarkSubmissionLoader,
)
from mcs-benchmark-data.paths import PROJECT_ROOT
from mcs-benchmark-data.pipeline.CommonsenseQA.CommonsenseQA_pipeline import (
    McsBenchmarkPipeline,
)
from mcs-benchmark-data.pipeline_storage import PipelineStorage


class CommonsenseQALoader(CompositeLoader):
    def __init__(self, bzip: bool = True):
        CompositeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, *args, **kwds):
        mcs_apps_dir_path = PROJECT_ROOT.parent / "mcs-apps"
        assert (
            mcs_apps_dir_path.is_dir()
        ), f"expected mcs-portal checkout at ${mcs_apps_dir_path}"

        storage = PipelineStorage(
            pipeline_id=McsBenchmarkPipeline.ID,
            root_data_dir_path=PROJECT_ROOT,
            loaded_data_dir_path=mcs_apps_dir_path
            / "app"
            / "benchmark"
            / "conf"
            / "data"
            / "import"
            / "benchmark",
        )
        self._loaders.append(JsonlBenchmarkLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkAnswerLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkQuestionLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkSubmissionLoader(bzip=self.__bzip).open(storage))
        return self