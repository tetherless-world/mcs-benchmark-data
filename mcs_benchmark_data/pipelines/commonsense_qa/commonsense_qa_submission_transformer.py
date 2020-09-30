import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class CommonsenseQaSubmissionTransformer(_Transformer):

    __URI_BASE = "benchmark:commonsense_qa"
    __BENCHMARK_SCORE_CLASSES={
        "TestScore": TestScore,
        "DevScore": DevScore
    }

    def transform(
        self,
        *,
        system: str,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_paths: Tuple[Path, ...],
        **kwds
    ) -> Generator[_Model, None, None]:

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        submission =  self.__transform_submission(submission_data_jsonl, system)

        yield submission

        for path in submission_jsonl_file_paths:
            dirs, fname = os.path.split(path)
            submission_system = fname.split("_")[-2]
            if submission_system = system:
                yield from self.__transform_submission_sample(
                    path, system, submission.uri
                )



    def __transform_submission(
        self, submission_data_jsonl_file_path, system:str
    ) -> Generator[Submission, None, None]:

        with open(submission_data_jsonl_file_path) as submission_data_jsonl:
            all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            submission_uri = "{}:submission:{}".format(self.__URI_BASE,submission["@id"])

            if submission["name"] != system:
                continue

            scores = []

            for item in submission["contentRating"]:

                score = self.__BENCHMARK_SCORE_CLASSES[item["type"]](
                    uri = "{}:{}".format(submission_uri,item["type"]),
                    isBasedOn=item["isBasedOn"],
                    name=item["name"],
                    value=item["value"],            
                )

                scores.append(score)

            yield Submission(
                uri=submission_uri,
                name=submission["@id"],
                description=submission["description"],
                dateCreated=submission["dateCreated"],
                isBasedOn=submission["isBasedOn"],
                contributors=tuple(
                    contributor["name"] for contributor in benchmark_metadata["authors"]
                ),
                contentRating=tuple(scores),
                resultOf=(
                    submission["resultOf"]["@type"],
                    strptime(submission["resultOf"]["startTime"], "%m-%d-%YT%H:%M:%SZ"),
                    strptime(submission["resultOf"]["endTime"], "%m-%d-%YT%H:%M:%SZ"),
                    submission["url"],
                )
            )

            for score in scores:
                yield score

            break

    def __transform_submission_sample(
        self, submission_sample_json, system: str, submission_uri: URIRef
    ) -> Generator[SubmissionSample, None, None]:

        all_samples = list(submission_sample_jsonl)

        for line in all_samples:

            sample = json.loads(line)

            yield SubmissionSample(
                uri="{}:sample:{}".format(submission_uri,sample["id"]),
                about="{}-{}".format(system,sample["id"]),
                #I do not think includedInDataset is correct.
                datasetURI=submission_uri,
                value=sample["chosenAnswer"]
            )
