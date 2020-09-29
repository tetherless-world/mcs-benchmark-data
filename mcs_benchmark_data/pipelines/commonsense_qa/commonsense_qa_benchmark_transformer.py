import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_answer import BenchmarkAnswer
from mcs_benchmark_data.models.benchmark_antecedent import BenchmarkAntecedent
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class CommonsenseQaBenchmarkTransformer(_Transformer):
    __TYPE = "@type"
    __LIST = "itemListElement"

    def transform(
        self,
        *,
        benchmark_json_file_path: Path,
        dev_jsonl_file_path: Path,
        test_jsonl_file_path: Path,
        train_jsonl_file_path: Path,
        submission_data_jsonl_file_path: Path,
        submission_jsonl_file_paths: Tuple[Path, ...]
    ) -> Generator[_Model, None, None]:

        benchmark_json = open(benchmark_json_file_path)
        yield from self.__transform_benchmark(benchmark_json)

        # Yield benchmark dev sample
        dev_json = open(dev_jsonl_file_path)
        yield from self.__transform_benchmark_sample(dev_json, "dev")

        # Yield benchmark train sample
        train_json = open(train_jsonl_file_path)
        yield from self.__transform_benchmark_sample(train_json, "train")

        # Yield submissions
        # Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        submission_data_jsonl = open(submission_data_jsonl_file_path)
        for path in submission_jsonl_file_paths:
            submission_json = open(path)
            dirs, fname = os.path.split(path)
            system = fname.split("_")[-2]
            yield from self.__transform_submission(submission_data_jsonl, submission_json, system)

    def __transform_benchmark(self, benchmark_json) -> Generator[_Model, None, None]:
        # benchmark_bootstrap = BenchmarkBoostrap.from_json(benchmark_json)
        benchmark_metadata = json.load(benchmark_json)

        benchmark_datasets = []
        
        for dataset in benchmark_metadata["datasets"]:
            new_dataset = BenchmarkDataset(uri=dataset["@id"], name=dataset["name"], entries=tuple())
            
            yield new_dataset

            benchmark_datasets.append(new_dataset)
        


        yield Benchmark(
            uri="",
            name=benchmark_metadata["name"],
            abstract=benchmark_metadata["abstract"],
            authors=tuple(str for author in benchmark_metadata["authors"]),
            datasets=tuple(benchmark_datasets),
            submissions=None
        )
        

    def __transform_benchmark_sample(
        self, sample_json, sample_type: str
    ) -> Generator[_Model, None, None]:

        question_type = BenchmarkQuestionType.MULTIPLE_CHOICE
        question_category = None
        included_in_dataset = "CommonsenseQA/{}".format(sample_type)

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        all_samples = list(sample_json)

        for line in all_samples:

            sample = json.loads(line)

            correct_choice = ans_mapping[sample["answerKey"]]

            concept = BenchmarkConcept(uri = "", concept=sample["question"]["question_concept"])

            yield concept

            choices_list = []

            for item in sample["question"]["choices"]:
                choice = BenchmarkChoice(
                    uri="",
                    position=item["label"],
                    text=item["text"],
                )
                choices_list.append(choice)
                yield choice

            choices = BenchmarkChoices(
                uri = "",
                choices=tuple(choices_list)
            )
            yield choices

            question = BenchmarkQuestion(
                uri="",
                text=sample["question"]["stem"],
                concepts=concept
            )
            yield question

            antecedent = BenchmarkAntecedent(
                uri="",
                elements=question
            )
            yield BenchmarkSample(
                uri=sample["id"],
                includedInDataset=included_in_dataset,
                questionType=question_type,
                questionCategory=question_category,
                antecedent=antecedent,
                choices=choices,
                correctChoice=correct_choice,
            )

    def __transform_submission(
        self, submission_data_jsonl, submission_json, system: str
    ) -> Generator[Submission, None, None]:
        
        all_submissions = list(submission_data_jsonl)

        for line in all_submissions:

            submission = json.loads(line)

            if submission["name"] != "system":
                continue

            scores = []

            for item in submission["contentRating"]:

                score = None
                
                if item["type"] == "TestScore":
                    score = Test_Score(
                        isBasedOn=item["isBasedOn"],
                        name=item["name"],
                        value=item["value"]
                    )
                
                elif item["type"] == "DevScore":
                    score = Test_Score(
                        isBasedOn=item["isBasedOn"],
                        name=item["name"],
                        value=item["value"]
                    )

                yield score

                scores.append(score)


            yield Submission(
                uri="",
                name = submission["@id"],
                description = submission["description"],
                dateCreated = submission["dateCreated"],
                isBasedOn = submission["isBasedOn"],
                contributors=tuple(contributor["name"] for contributor in benchmark_metadata["authors"]),
                contentRating=tuple(scores),
                resultOf=(submission["resultOf"]["@type"], strptime(submission["resultOf"]["startTime"], "%m-%d-%YT%H:%M:%SZ"), strptime(submission["resultOf"]["endTime"], "%m-%d-%YT%H:%M:%SZ"), submission["url"])
                #Samples?
            )

            break

    def __transform_submission_sample(
        self, submission_sample_json
    ) -> Generator[BenchmarkAnswer, None, None]:
        yield BenchmarkAnswer(
            uri="",
            text=submission_sample_json["value"],
            position=submission_sample_json["position"],
        )
