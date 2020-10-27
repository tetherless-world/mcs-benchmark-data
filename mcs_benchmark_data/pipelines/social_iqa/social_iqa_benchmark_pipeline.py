from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.benchmark_extractor import (
    BenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_transformer import (
    SocialIQaBenchmarkTransformer,
)
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_file_names import (
    SocialIQaBenchmarkFileNames,
)


class SocialIQaBenchmarkPipeline(_Pipeline):
    ID = "SocialIQA"

    def __init__(self, file_names: SocialIQaBenchmarkFileNames, **kwds):
        _Pipeline.__init__(
            self,
            extractor=BenchmarkExtractor(
                pipeline_id=self.ID,
                file_names=file_names,
                **kwds,
            ),
            id=self.ID,
            transformer=SocialIQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    SocialIQaBenchmarkPipeline.main()