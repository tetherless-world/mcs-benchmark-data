import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class CommonsenseQaSubmissionTransformer(_Transformer):

    def transform(
        self,
        *,
        system: str,
        benchmark_json_file_path: Path,
        dev_jsonl_file_path: Path,
        test_jsonl_file_path: Path,
        train_jsonl_file_path: Path,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_paths: Tuple[Path, ...]
    ) -> Generator[_Model, None, None]:

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        submission_data_jsonl = open(submission_data_jsonl_file_path)
        yield from self.__transform_submission(submission_data_jsonl, system)

        for path in submission_jsonl_file_paths:
            submission_jsonl = open(path)
            dirs, fname = os.path.split(path)
            submission_system = fname.split("_")[-2]
            if submission_system = system:
                yield from self.__transform_submission_sample(
                    submission_jsonl, system
                )


    def __transform_submission(
        self, submission_data_jsonl, system:str
    ) -> Generator[Submission, None, None]:

        all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if submission["name"] != system:
                continue

            scores = []

            for item in submission["contentRating"]:

                score = None

                if item["type"] == "TestScore":
                    score = Test_Score(
                        isBasedOn=item["isBasedOn"],
                        name=item["name"],
                        value=item["value"],
                    )

                elif item["type"] == "DevScore":
                    score = Test_Score(
                        isBasedOn=item["isBasedOn"],
                        name=item["name"],
                        value=item["value"],
                    )

                yield score

                scores.append(score)

            yield Submission(
                uri="",
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

            break

    def __transform_submission_sample(
        self, submission_sample_json, system: str
    ) -> Generator[SubmissionSample, None, None]:

        all_samples = list(submission_sample_jsonl)

        for line in all_samples:

            sample = json.loads(line)

            yield SubmissionSample(
                uri="{}-{}-submission".format(system,sample["id"]),
                about="{}-{}".format(system,sample["id"]),
                #I do not think includedInDataset is correct.
                includedInDataset=sample["id"],
                value=sample["chosenAnswer"]
            )
