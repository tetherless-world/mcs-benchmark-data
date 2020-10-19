from mcs_benchmark_data._pipeline import _Pipeline

from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_extractor import (
    PhysicalIQaBenchmarkExtractor,
)
from mcs_benchmark_data.pipelines.physical_iqa.physical_iqa_benchmark_transformer import (
    PhysicalIQaBenchmarkTransformer,
)


class PhysicalIQaBenchmarkPipeline(_Pipeline):
    ID = "PhysicalIQa"

    def __init__(
        self,
        dev_jsonl_file_name="dev.jsonl",
        dev_labels_file_name="dev-labels.lst",
        test_jsonl_file_name="test.jsonl",
        train_jsonl_file_name="train.jsonl",
        train_labels_file_name="train-labels.lst",
        **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=PhysicalIQaBenchmarkExtractor(
                pipeline_id=self.ID,
                dev_jsonl_file_name=dev_jsonl_file_name,
                dev_labels_file_name=dev_labels_file_name,
                test_jsonl_file_name=test_jsonl_file_name,
                train_jsonl_file_name=train_jsonl_file_name,
                train_labels_file_name=train_labels_file_name,
                **kwds,
            ),
            id=self.ID,
            transformer=PhysicalIQaBenchmarkTransformer(pipeline_id=self.ID, **kwds),
            **kwds,
        )


if __name__ == "__main__":
    PhysicalIQaBenchmarkPipeline.main()
