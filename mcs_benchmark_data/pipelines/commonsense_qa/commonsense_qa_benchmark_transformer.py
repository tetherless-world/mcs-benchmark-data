import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.models.benchmark_antecedent import BenchmarkAntecedent
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_train_dataset import BenchmarkTrainDataset
from mcs_benchmark_data.models.benchmark_test_dataset import BenchmarkTestDataset
from mcs_benchmark_data.models.benchmark_dev_dataset import BenchmarkDevDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample


class CommonsenseQaBenchmarkTransformer(_Transformer):

    __URI_BASE = "benchmark:commonsense_qa"
    __BENCHMARK_DATASET_CLASSES = {
        "dev": BenchmarkDevDataset,
        "test": BenchmarkTestDataset,
        "train": BenchmarkTrainDataset,
    }

    def transform(
        self, benchmark_json_file_path: Path, **kwds
    ) -> Generator[_Model, None, None]:

        with open(benchmark_json_file_path) as benchmark_json:
            benchmark_metadata = json.load(benchmark_json)

        benchmark_datasets = []

        for dataset in benchmark_metadata["datasets"]:

            dataset_type = dataset["@id"].split("/")[-1]

            dataset_uri = "{}:dataset:{}".format(self.__URI_BASE, dataset["@id"])

            new_dataset = self.__BENCHMARK_DATASET_CLASSES[dataset_type](
                uri=dataset_uri, type=dataset_type, name=dataset["name"]
            )

            benchmark_datasets.append(new_dataset)

            yield from self.__transform_benchmark_sample(
                kwds[dataset_type + "_jsonl_file_path"], dataset_type, new_dataset.uri
            )

        benchmark = Benchmark(
            uri="{}:benchmark:{}".format(self.__URI_BASE, benchmark_metadata["@id"]),
            name=benchmark_metadata["name"],
            abstract=benchmark_metadata["abstract"],
            authors=tuple(str for author in benchmark_metadata["authors"]),
            datasets=tuple(benchmark_datasets),
        )

        yield benchmark

        for dataset in benchmark_datasets:
            yield dataset

    def __transform_benchmark_sample(
        self, sample_jsonl_file_path, sample_type: str, dataset_uri: URIRef
    ) -> Generator[_Model, None, None]:

        with open(sample_jsonl_file_path) as sample_jsonl:
            all_samples = list(sample_jsonl)

        question_type = BenchmarkQuestionType.MULTIPLE_CHOICE
        question_category = None

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        for line in all_samples:

            sample = json.loads(line)

            benchmark_sample_uri = "{}:sample:{}".format(dataset_uri, sample["id"])

            correct_choice = None

            if sample_type != "test":
                correct_choice = ans_mapping[sample["answerKey"]]

            concept = BenchmarkConcept(
                uri="{}:concept".format(benchmark_sample_uri),
                concept=sample["question"]["question_concept"],
            )

            choices_list = []

            for item in sample["question"]["choices"]:
                choice = BenchmarkChoice(
                    uri="{}:choice:{}: ".format(benchmark_sample_uri, item["label"]),
                    position=item["label"],
                    text=item["text"],
                )
                choices_list.append(choice)

            choices = BenchmarkChoices(
                uri="{}:choices".format(benchmark_sample_uri),
                choices=tuple(choices_list),
            )

            question = BenchmarkQuestion(
                uri="{}:question".format(benchmark_sample_uri),
                text=sample["question"]["stem"],
                concepts=concept,
            )

            antecedent = BenchmarkAntecedent(
                uri="{}:antecedent".format(benchmark_sample_uri), elements=question
            )
            yield BenchmarkSample(
                uri=sample["id"],
                datasetURI=dataset_uri,
                questionType=question_type,
                questionCategory=question_category,
                antecedent=antecedent,
                choices=choices,
                correctChoice=correct_choice,
            )

            yield question
            yield choices

            for item in choices_list:
                yield choice

            yield antecedent
            yield concept
