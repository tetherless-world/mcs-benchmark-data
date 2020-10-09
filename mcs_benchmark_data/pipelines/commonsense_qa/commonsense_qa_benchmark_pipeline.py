from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_extractor import (
    CommonsenseQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_transformer import (
    CommonsenseQaBenchmarkTransformer,
)


class CommonsenseQaBenchmarkPipeline(_Pipeline):
    ID = "CommonsenseQA"

    def __init__(
        self,
        dev_jsonl_file="dev_rand_split.jsonl",
        test_jsonl_file="test_rand_split_no_answers.jsonl",
        train_jsonl_file="train_rand_split.jsonl",
        **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=CommonsenseQaBenchmarkExtractor(
                pipeline_id=self.ID,
                dev_jsonl_file=dev_jsonl_file,
                test_jsonl_file=test_jsonl_file,
                train_jsonl_file=train_jsonl_file,
                **kwds,
            ),
            id=self.ID,
            transformer=CommonsenseQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    CommonsenseQaBenchmarkPipeline.main()
