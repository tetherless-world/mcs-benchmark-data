import json
from time import strptime
from pathlib import Path
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_submission_transformer import (
    _BenchmarkSubmissionTransformer,
)


class KagnetCommonsenseQaSubmissionTransformer(_BenchmarkSubmissionTransformer):

    """
    Class for transforming CommonsenseQA kagnet sample.
    """

    def transform(
        self,
        *,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_path: Path,
        **kwds,
    ) -> Generator[_Model, None, None]:

        yield from self._transform(
            submission_data_jsonl_file_path=submission_data_jsonl_file_path,
            submission_jsonl_file_path=submission_jsonl_file_path,
            submission_name="kagnet",
        )
