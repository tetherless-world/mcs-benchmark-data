import json
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._benchmark_transformer import _BenchmarkTransformer
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.answer_data import AnswerData
from mcs_benchmark_data.dataset_type import DatasetType
from mcs_benchmark_data.infile_labels_benchmark_file_names import (
    InfileLabelsBenchmarkFileNames,
)


class SocialIQaBenchmarkTransformer(_BenchmarkTransformer):
    def _transform_benchmark_sample(
        self,
        *,
        extracted_data_dir_path: Path,
        file_names: InfileLabelsBenchmarkFileNames,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]:

        all_labels = None

        if dataset_type != DatasetType.TEST.value:
            sample_labels_file_path = (
                extracted_data_dir_path
                / "datasets"
                / dataset_type
                / getattr(file_names, dataset_type + "_labels")
            )

            with open(sample_labels_file_path) as labels_file:
                all_labels = list(labels_file)

        sample_jsonl_file_path = (
            extracted_data_dir_path
            / "datasets"
            / dataset_type
            / getattr(file_names, dataset_type + "_samples")
        )

        with open(sample_jsonl_file_path) as all_samples:

            for i, (line, label) in enumerate(zip(all_samples, all_labels)):

                sample = json.loads(line)

                benchmark_sample_uri = URIRef(f"{dataset_uri}:sample:{i}")

                correct_choice = None

                if dataset_type != DatasetType.TEST.value:
                    correct_choice = URIRef(
                        f"{dataset_uri}:sample:{i}:correct_choice:{int(label) + 1}"
                    )

                yield BenchmarkQuestionType.multiple_choice(
                    uri_base=self._uri_base,
                    benchmark_sample_uri=benchmark_sample_uri,
                )

                yield from self._yield_sample_concept_context(
                    dataset_uri=dataset_uri,
                    sample_id=i,
                    concepts=None,
                    context=sample["context"],
                    correct_choice=correct_choice,
                )

                yield from self._yield_qa_models(
                    dataset_uri=dataset_uri,
                    sample_id=i,
                    benchmark_sample_uri=benchmark_sample_uri,
                    question=sample["question"],
                    answers=(
                        AnswerData(label=letter, text=sample[f"answer{letter}"])
                        for letter in ["A", "B", "C"]
                    ),
                )
