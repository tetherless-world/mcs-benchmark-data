import json
from time import strptime
from pathlib import Path
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_submission_transformer import (
    _BenchmarkSubmissionTransformer,
)
from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)


class KagnetCommonsenseQaSubmissionTransformer(_BenchmarkSubmissionTransformer):

    """
    Class for transforming CommonsenseQA kagnet sample.
    """

    def transform(
        self,
        *,
        extracted_path: Path,
        file_names: KagnetCommonsenseQaSubmissionFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:

        yield from self._transform(
            extracted_path=extracted_path,
            file_names=file_names,
            submission_name="kagnet",
            **kwds,
        )
