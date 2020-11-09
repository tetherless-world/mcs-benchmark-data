from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.path import TEST_DATA_DIR_PATH

from mcs_benchmark_data.nop_extractor import (
    NopExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)


class CommonsenseQaBenchmarkPipeline(_Pipeline):
    ID = "commonsense_qa"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(pipeline_id=self.ID, **kwds),
            id=self.ID,
            transformer=CommonsenseQaBenchmarkTransformer(
                pipeline_id=self.ID, data_dir_path=TEST_DATA_DIR_PATH, **kwds
            ),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaBenchmarkPipeline.main()
