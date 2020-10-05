import json
from time import strptime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.pipelines.commonsense_qa._commonsense_qa_submission_transformer import (
    _CommonsenseQaSubmissionTransformer,
)
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class KagnetCommonsenseQaSubmissionTransformer(_CommonsenseQaSubmissionTransformer):

    """
    Class for transforming CommonsenseQA kagnet sample.
    """

    def transform(
        self,
        *,
        system: str,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_path: Path,
        **kwds
    ) -> Generator[_Model, None, None]:

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_kagnet_submission.jsonl)
        submission = yield self.__transform_submission(submission_data_jsonl_file_path)

        yield submission

        yield from self.__transform_submission_sample(
            submission_jsonl_file_path, submission.uri
        )

    def __transform_submission(
        self, submission_data_jsonl_file_path: Path
    ) -> Generator[_Model, None, None]:

        with open(submission_data_jsonl_file_path) as submission_data_jsonl:
            all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if submission["name"].lower() != "kagnet":
                continue

            submission_obj = Submission(
                uri="{}:submission:{}".format(self.__URI_BASE, submission["@id"]),
                name=submission["@id"],
                description=submission["description"],
                date_created=submission["dateCreated"],
                is_based_on=submission["isBasedOn"],
                contributors=tuple(
                    contributor["name"] for contributor in submission["contributor"]
                ),
                result_of=(
                    submission["resultOf"]["@type"],
                    strptime(submission["resultOf"]["startTime"], "%m-%d-%YT%H:%M:%SZ"),
                    strptime(submission["resultOf"]["endTime"], "%m-%d-%YT%H:%M:%SZ"),
                    submission["url"],
                ),
            )

            yield submission_obj

            for item in submission["contentRating"]:

                score = self.__BENCHMARK_SCORE_CLASSES[item["type"]](
                    uri="{}:{}".format(submission_obj.uri, item["type"]),
                    submission_uri=submission_obj.uri,
                    is_based_on=item["isBasedOn"],
                    name=item["name"],
                    value=item["value"],
                )

                yield score

            break

    def __transform_submission_sample(
        self, submission_sample_jsonl_file_path: Path, submission_uri: URIRef
    ) -> Generator[_Model, None, None]:

        all_samples = list(submission_sample_jsonl_file_path)

        for line in all_samples:

            sample = json.loads(line)

            yield SubmissionSample(
                uri="{}:sample:{}".format(submission_uri, sample["id"]),
                submission_uri=submission_uri,
                value=sample["chosenAnswer"],
                about="kagnet-{}".format(sample["id"]),
            )
