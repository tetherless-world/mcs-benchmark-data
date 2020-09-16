from mcs-benchmark-data._pipeline import _Pipeline


class CommonsenseQAPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(self, bzip: bool = True, **kwargs):
        from mcs-benchmark-data.pipeline.CommonsenseQA.CommonsenseQA_extractor import (
            McsBenchmarkExtractor,
        )
        from mcs-benchmark-data.pipeline.CommonsenseQA.CommonsenseQA_loader import (
            McsBenchmarkLoader,
        )
        from mcs-benchmark-data.pipeline.CommonsenseQA.CommonsenseQA_transformer import (
            McsBenchmarkTransformer,
        )

        _Pipeline.__init__(
            self,
            extractor=CommonsenseQAExtractor(),
            id=self.ID,
            loader=CommonsenseQALoader(bzip=bzip),
            transformer=CommonsenseQATransformer(),
        )