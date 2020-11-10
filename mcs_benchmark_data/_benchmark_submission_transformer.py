import json
from time import strptime
from pathlib import Path
from typing import Generator, Dict
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class _BenchmarkSubmissionTransformer(_Transformer):

    """
    Abstract base class for benchmark submissions.
    See the transform method of _Transformer.
    """

    def __init__(self, *, pipeline_id: str, submission_id: str, **kwds):
        _Transformer.__init__(self, pipeline_id=pipeline_id, **kwds)
        self._submission_id = submission_id

    @property
    def _uri_base(self):
        return f"benchmark:submission:{self._pipeline_id}"

    @property
    def _benchmark_score_classes(self):
        return {"TestScore": TestScore, "DevScore": DevScore}

    def _read_jsonl_file(
        self,
        jsonl_file_path: Path,
    ) -> Generator[Dict[str, object], None, None]:
        with open(jsonl_file_path) as jsonl_file:
            for line in jsonl_file:
                if not line.strip():
                    continue
                yield json.loads(line)

    def transform(
        self,
        **kwds,
    ) -> Generator[_Model, None, None]:

        submission_data_jsonl_file_path = (
            self._pipeline_data_dir_path / "submissions" / "submissions_metadata.jsonl"
        )

        # Yield submissions
        yield from self.__transform_submission(
            submission_data_jsonl_file_path=submission_data_jsonl_file_path,
        )

        submission_uri = URIRef(f"{self._uri_base}:submission:{self._pipeline_id}")

        yield from getattr(self, f"_transform_{self._pipeline_id}_submission_sample")(
            submission_uri=submission_uri,
        )

    def __transform_submission(
        self,
        submission_data_jsonl_file_path: Path,
    ) -> Generator[_Model, None, None]:

        for submission_line in self._read_jsonl_file(submission_data_jsonl_file_path):

            if self._submission_id not in submission_line["name"].lower():
                continue

            submission = Submission(
                uri=URIRef(f"{self._uri_base}:submission:{self._pipeline_id}"),
                name=f"{self._pipeline_id}-{self._submission_id}",
                description=submission_line["description"],
                date_created=submission_line["dateCreated"],
                is_based_on=submission_line["isBasedOn"],
                contributors=tuple(submission_line["contributor"]["name"]),
                result_of=(
                    submission_line["resultOf"]["@type"],
                    strptime(
                        submission_line["resultOf"]["startTime"], "%m-%d-%YT%H:%M:%SZ"
                    ),
                    strptime(
                        submission_line["resultOf"]["endTime"], "%m-%d-%YT%H:%M:%SZ"
                    ),
                    submission_line["resultOf"]["url"],
                ),
            )

            yield submission

            for item in submission_line["contentRating"]:

                score = self._benchmark_score_classes[item["@type"]](
                    uri=URIRef(f"{submission.uri}:{item['@type']}"),
                    submission_uri=submission.uri,
                    is_based_on=item["isBasedOn"],
                    name=item["name"],
                    value=item["value"],
                )

                yield score

            break

    def _transform_commonsense_qa_submission_sample(
        self,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        submission_sample_file_path = (
            self._pipeline_data_dir_path
            / "submissions"
            / self._submission_id
            / f"{self._submission_id}_dev_submission.jsonl"
        )

        for sample in self._read_jsonl_file(submission_sample_file_path):

            yield SubmissionSample(
                uri=URIRef(f"{submission_uri}:sample:{sample['id']}"),
                submission_uri=submission_uri,
                value=sample["chosenAnswer"],
                about=f"{self._submission_id}-{sample['id']}",
            )

    def _transform_cycic_submission_sample(
        self,
        submission_uri: URIRef,
    ) -> Generator[_Model, None, None]:

        submission_sample_file_path = (
            self._pipeline_data_dir_path
            / "submissions"
            / self._submission_id
            / f"{self._submission_id}_dev_submission.jsonl"
        )

        for sample in self._read_jsonl_file(submission_sample_file_path):

            yield SubmissionSample(
                uri=URIRef(f"{submission_uri}:sample:{sample['example_id']}"),
                submission_uri=submission_uri,
                value=sample["pred"],
                about=f"{self._submission_id}-{sample['example_id']}",
            )
