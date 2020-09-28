from datetime import datetime
from typing import Dict, Optional, Tuple, Generator
from pathlib import Path
from urllib.parse import quote_plus
import json 
import os

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.namespace import MCS, SCHEMA
from mcs_benchmark_data.models.benchmark import Benchmark
from mcs_benchmark_data.models.benchmark_bootstrap import BenchmarkBootstrap
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices
from mcs_benchmark_data.models.submission import Submission
from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType

class CommonsenseQaTransformer(_Transformer):
    __TYPE = "@type"
    __LIST = "itemListElement"

    def transform(self, *, benchmark_json_file_path: Path, dev_json_file_path: Path,
     train_json_file_path: Path, submission_json_file_paths: Tuple[Path]
    ) -> Generator[_Model, None, None]:
        benchmark_json = open(benchmark_json_file_path)
        self.__transform_benchmark(benchmark_json_file_path)

        #Yield benchmark dev sample
        dev_json = open(dev_json_file_path)
        self.__transform_benchmark_sample(dev_json, "dev")

        #Yield benchmark train sample
        train_json = open(train_json_file_path)
        self.__transform_benchmark_sample(train_json, "train")

        #Yield submissions
        #Assumes file name in form "*_[systemname]_submission.jsonl" (e.g. dev_rand_split_roberta_submission.jsonl)
        for path in submission_json_file_paths:
            submission_json = open(path)
            dirs, fname = os.path.split(path)
            system = fname.split("_")[-2]
            self.__transform_submission(submission_json, system)

    def __transform_benchmark(self, benchmark_json):
        #benchmark_bootstrap = BenchmarkBoostrap.from_json(benchmark_json)
        benchmark_metadata = json.loads(benchmark_json)
        yield Benchmark(
            name=benchmark_metadata['name'],
            abstract=benchmark_metadata.abstract,
            authors=tuple(
                str
                for author in benchmark_metadata['authors']
            ),
            datasets=tuple(
                BenchmarkDataset(uri=dataset["@id"], name=dataset["name"])
                for dataset in benchmark_metadata["dataset"]
            )
        )

    def __transform_benchmark_sample(
        self, sample_json, sample_type: str
    ) -> Generator[BenchmarkSample, None, None]:

        question_type = BenchmarkQuestionType.MULTIPLE_CHOICE
        question_category = None
        included_in_dataset = "CommonsenseQA/{}".format(sample_type)

        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}

        for line in sample_json:
            sample = json.loads(line)

            correct_choice = ans_mapping[sample["answerKey"]]

            concept = BenchmarkConcept(
                concept=sample["question"]["question_concept"]
            )

            choices_list = []

            for item in sample_json["question"]["choices"][self.__LIST]:
                choice = BenchmarkChoice(
                        uri=,
                        position=item["label"],
                        text=item["text"],
                    )
                choices_list.append(choice)
                yield choice

            choices = BenchmarkChoices(
                uri = ,
                choices=Tuple(choices_list)
            )
            yield choices

            question = BenchmarkQuestion(
                uri=,
                text=sample_json["question"]["stem"]
                concept=concept
            )
            yield question

            antecedent = BenchmarkAntecedent(
                uri=,
                elements=Tuple[question]
            )
            yield BenchmarkSample(
                uri = sample_json["@id"],
                includedInDataset=included_in_dataset,
                questionType=question_type,
                questionCategory=question_category,
                antecedent=antecedent,
                choices=choices,
                correctChoice=correct_choice
            )

    def __transform_submission(
        self, submission_json, system: str
    ) -> Generator[BenchmarkSubmission, None, None]:
        name = "CommonsenseQA-{}".format(system)
        description = ""
        dateCreated = datetime.today()
        isBasedOn = "CommonsenseQA"


    def __transform_submission_sample(
        self, submission_sample_json
    ) -> Generator[BenchmarkAnswer, None, None]:


        yield BenchmarkAnswer(
            text=submission_sample_json["value"],
            position=submission_sample_json["position"]
        )