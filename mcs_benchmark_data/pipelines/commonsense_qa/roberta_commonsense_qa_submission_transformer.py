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


class RobertaCommonsenseQaSubmissionTransformer(_CommonsenseQaSubmissionTransformer):
    """
    Class for transforming CommonsenseQA roberta sample.
    """

    __URI_BASE = "benchmark:commonsense_qa"
    __BENCHMARK_SCORE_CLASSES = {"TestScore": TestScore, "DevScore": DevScore}

    def transform(
        self,
        *,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_path: Path,
        **kwds,
    ) -> Generator[_Model, None, None]:

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        yield from self.__transform_submission(submission_data_jsonl_file_path)

        submission_uri = URIRef(f"{self.__URI_BASE}:submission:CommonsenseQA-roberta")

        yield from self.__transform_submission_sample(
            submission_jsonl_file_path, submission_uri
        )

    def __transform_submission(
        self, submission_data_jsonl_file_path: Path
    ) -> Generator[_Model, None, None]:

        with open(submission_data_jsonl_file_path) as submission_data_jsonl:
            all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if submission["name"].lower() != "roberta":
                continue

            submission_obj = Submission(
                uri=URIRef(f"{self.__URI_BASE}:submission:{submission['@id']}"),
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

                score = self.__BENCHMARK_SCORE_CLASSES[item["@type"]](
                    uri=URIRef(f"{submission_obj.uri}:{item['@type']}"),
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

        with open(submission_sample_jsonl_file_path) as submission_sample_jsonl:
            all_samples = list(submission_sample_jsonl)

        for line in all_samples:

            sample = json.loads(line)

            yield SubmissionSample(
                uri=URIRef(f"{submission_uri}:sample:{sample['id']}"),
                submission_uri=submission_uri,
                value=sample["chosenAnswer"],
                about=f"roberta-{sample['id']}",
            )
