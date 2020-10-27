import json
import os
from time import strptime
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore
from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


class _BenchmarkSubmissionTransformer(_Transformer):

    """
    Abstract base class for benchmark submissions.
    See the transform method of _Transformer.
    """

    @property
    def _uri_base(self):
        return f"benchmark:submission:{self._pipeline_id}"

    @property
    def _benchmark_score_classes(self):
        return {"TestScore": TestScore, "DevScore": DevScore}

    def _transform(
        self,
        *,
        extracted_path: Path,
        file_names: _BenchmarkFileNames,
        submission_name: str,
        **kwds,
    ) -> Generator[_Model, None, None]:

        submission_data_jsonl_file_path = extracted_path / getattr(
            file_names, "metadata"
        )

        submission_jsonl_file_path = extracted_path / getattr(
            file_names, "submission_file_name"
        )

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        yield from self.__transform_submission(
            submission_data_jsonl_file_path=submission_data_jsonl_file_path,
            submission_name=submission_name,
        )

        submission_uri = URIRef(
            f"{self._uri_base}:submission:{self._pipeline_id}-{submission_name}"
        )

        yield from self.__transform_submission_sample(
            submission_sample_jsonl_file_path=submission_jsonl_file_path,
            submission_uri=submission_uri,
            submission_name=submission_name,
        )

    def __transform_submission(
        self,
        submission_data_jsonl_file_path: Path,
        submission_name: str,
    ) -> Generator[_Model, None, None]:

        with open(submission_data_jsonl_file_path) as submission_data_jsonl:
            all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if submission["name"].lower() != submission_name:
                continue

            submission_obj = Submission(
                uri=URIRef(f"{self._uri_base}:submission:{submission['@id']}"),
                name=submission["@id"],
                description=submission["description"],
                date_created=submission["dateCreated"],
                is_based_on=submission["isBasedOn"],
                contributors=tuple(submission["contributor"]["name"]),
                result_of=(
                    submission["resultOf"]["@type"],
                    strptime(submission["resultOf"]["startTime"], "%m-%d-%YT%H:%M:%SZ"),
                    strptime(submission["resultOf"]["endTime"], "%m-%d-%YT%H:%M:%SZ"),
                    submission["resultOf"]["url"],
                ),
            )

            yield submission_obj

            for item in submission["contentRating"]:

                score = self._benchmark_score_classes[item["@type"]](
                    uri=URIRef(f"{submission_obj.uri}:{item['@type']}"),
                    submission_uri=submission_obj.uri,
                    is_based_on=item["isBasedOn"],
                    name=item["name"],
                    value=item["value"],
                )

                yield score

            break

    def __transform_submission_sample(
        self,
        submission_sample_jsonl_file_path: Path,
        submission_uri: URIRef,
        submission_name: str,
    ) -> Generator[_Model, None, None]:

        with open(submission_sample_jsonl_file_path) as submission_sample_jsonl:
            all_samples = list(submission_sample_jsonl)

        for line in all_samples:

            sample = json.loads(line)

            yield SubmissionSample(
                uri=URIRef(f"{submission_uri}:sample:{sample['id']}"),
                submission_uri=submission_uri,
                value=sample["chosenAnswer"],
                about=f"{submission_name}-{sample['id']}",
            )
