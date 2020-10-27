import json
from time import strptime
from pathlib import Path
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_submission_transformer import (
    _BenchmarkSubmissionTransformer,
)
from mcs_benchmark_data.pipelines.cycic.roberta4_cycic_submission_file_names import (
    Roberta4CycicSubmissionFileNames,
)


class Roberta4CycicSubmissionTransformer(_BenchmarkSubmissionTransformer):

    """
    Class for transforming CommonsenseQA kagnet sample.
    """

    def transform(
        self,
        *,
        extracted_path: Path,
        file_names: Roberta4CycicSubmissionFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:

        yield from self._transform(
            extracted_path=extracted_path,
            file_names=file_names,
            submission_name="roberta4",
            **kwds,
        )
