from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._benchmark_submission_transformer import (
    _BenchmarkSubmissionTransformer,
)

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.submission_sample import SubmissionSample


class TrianMCScriptSubmissionTransformer(_BenchmarkSubmissionTransformer):

    """
    Class for transforming MCScript Trian sample.
    """

    def _transform_mcscript_submission_sample(
        self,
        submission_sample_file_path: Path,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        with open(submission_sample_file_path) as submission_sample_text:

            for line in submission_sample_text:

                sample = line.split(",")

                sample_id = f"{sample[0]}-{sample[1]}"

                prediction = sample[2]

                yield SubmissionSample(
                    uri=URIRef(f"{submission_uri}:sample:{sample_id}"),
                    submission_uri=submission_uri,
                    value=prediction,
                    about=f"{self._submission_id}-{sample_id}",
                )
