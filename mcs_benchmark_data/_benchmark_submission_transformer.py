import json
import os
from time import strptime
from pathlib import Path
from abc import abstractmethod
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore
from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames
from mcs_benchmark_data._pipeline_phase import _PipelinePhase


class _BenchmarkSubmissionTransformer(_Transformer):

    """
    Abstract base class for benchmark submissions.
    See the transform method of _Transformer.
    """

    def __init__(self, *, pipeline_id: str, submission_name: str, **kwds):
        _Transformer.__init__(self, pipeline_id=pipeline_id, **kwds)
        self._submission_name = submission_name

    @property
    def _uri_base(self):
        return f"benchmark:submission:{self._pipeline_id}"

    @property
    def _benchmark_score_classes(self):
        return {"TestScore": TestScore, "DevScore": DevScore}

    def transform(
        self,
        *,
        extracted_data_dir_path: Path,
        file_names: _BenchmarkFileNames,
        **kwds,
    ) -> Generator[_Model, None, None]:

        submission_data_jsonl_file_path = extracted_data_dir_path / getattr(
            file_names, "metadata"
        )

        submission_jsonl_file_path = (
            extracted_data_dir_path
            / self._submission_name
            / getattr(file_names, "submission")
        )

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        yield from self.__transform_submission(
            submission_data_jsonl_file_path=submission_data_jsonl_file_path,
        )

        submission_uri = URIRef(
            f"{self._uri_base}:submission:{self._pipeline_id}-{self._submission_name}"
        )

        yield from getattr(
            self, f"_transform_{self._pipeline_id.lower()}_submission_sample"
        )(
            submission_sample_jsonl_file_path=submission_jsonl_file_path,
            submission_uri=submission_uri,
        )

    def __transform_submission(
        self,
        submission_data_jsonl_file_path: Path,
    ) -> Generator[_Model, None, None]:

        with open(submission_data_jsonl_file_path) as submission_data_jsonl:
            all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if self._submission_name not in submission["name"].lower():
                continue

            submission_obj = Submission(
                uri=URIRef(
                    f"{self._uri_base}:submission:{self._pipeline_id}-{self._submission_name}"
                ),
                name=f"{self._pipeline_id}-{self._submission_name}",
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

    def _transform_commonsenseqa_submission_sample(
        self,
        submission_sample_jsonl_file_path: Path,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        with open(submission_sample_jsonl_file_path) as submission_sample_jsonl:

            for line in submission_sample_jsonl:

                sample = json.loads(line)

                yield SubmissionSample(
                    uri=URIRef(f"{submission_uri}:sample:{sample['id']}"),
                    submission_uri=submission_uri,
                    value=sample["chosenAnswer"],
                    about=f"{self._submission_name}-{sample['id']}",
                )

    def _transform_mcscript_submission_sample(
        self,
        submission_sample_jsonl_file_path: Path,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        with open(submission_sample_jsonl_file_path) as submission_sample_jsonl:

            for line in submission_sample_jsonl:

                sample = json.loads(line)

                yield SubmissionSample(
                    uri=URIRef(
                        f"{submission_uri}:sample:{sample['sample_id']}_{sample['question_id']}"
                    ),
                    submission_uri=submission_uri,
                    value=sample["pred"],
                    about=f"{self._submission_name}-{sample['sample_id']}_{sample['question_id']}",
                )

    def _transform_cycic_submission_sample(
        self,
        submission_sample_jsonl_file_path: Path,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        with open(submission_sample_jsonl_file_path) as submission_sample_jsonl:

            for line in submission_sample_jsonl:

                sample = json.loads(line)

                yield SubmissionSample(
                    uri=URIRef(f"{submission_uri}:sample:{sample['example_id']}"),
                    submission_uri=submission_uri,
                    value=sample["pred"],
                    about=f"{self._submission_name}-{sample['example_id']}",
                )
