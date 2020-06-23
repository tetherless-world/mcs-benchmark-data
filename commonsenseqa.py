
import os
import json
from benchmark import Benchmark


class CommonsenseQA(Benchmark):
    def __init__(self, question_set_id):
        super(CommonsenseQA, self).__init__()
        self.question_set_id = question_set_id
        self.benchmark_id = "CommonsenseQA"
        self.samples = []
        self.labels = dict()
        self.chosen_labels = dict()

    def load_question_file(self, path):
        self.samples = []
        with open(path) as f:
            for line in f:
                self.samples.append(json.loads(line.strip()))

    def load_label_file(self, path):
        self.labels = dict()
        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}
        with open(path) as f:
            for line in f:
                sample = json.loads(line.strip())
                self.labels[sample["id"]] = ans_mapping[sample["answerKey"]]

    def load_chosen_label_file(self, path):
        self.chosen_labels = dict()
        ans_mapping = {ans: i for i, ans in enumerate("ABCDE")}
        with open(path) as f:
            for line in f:
                sample = json.loads(line.strip())
                self.chosen_labels[sample["id"]] = ans_mapping[sample["chosenAnswer"]]

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_samples(self):
        return self.samples

    def get_question_type(self, sample):
        return "multiple choice"

    def get_question_id(self, sample):
        return sample["id"]

    def get_question_set_id(self, sample):
        return self.question_set_id

    def get_question_text(self, sample):
        return sample["question"]["stem"]

    def get_question_concept(self, sample):
        return sample["question"]["question_concept"]

    def get_correct_choice(self, sample):
        if self.get_question_id(sample) not in self.labels:
            return None
        return self.labels[self.get_question_id(sample)]

    def get_chosen_choice(self, sample):
        if self.get_question_id(sample) not in self.chosen_labels:
            return None
        return self.chosen_labels[self.get_question_id(sample)]

    def get_choices(self, sample):
        choices = []
        num_choices = 5
        for i in range(num_choices):
            choice = dict()
            choice["@type"] = "BenchmarkAnswer"
            choice["name"] = "Answer"
            choice["identifier"] = sample["question"]["choices"][i]["label"]
            choice["text"] = sample["question"]["choices"][i]["text"]
            choices.append(choice)
        return choices

    def get_choice_explanation(self, sample):
        choices = []
        num_choices = 5
        for i in range(num_choices):
            choice = dict()
            choice["@type"] = "BenchmarkAnswer"
            choice["name"] = "Answer"
            choice["identifier"] = sample["question"]["choices"][i]["label"]
            choice["text"] = sample["question"]["choices"][i]["text"]

            if "explanation" in sample["question"]["choices"][i]:
                explanation = dict()
                explanation["@type"] = "BenchmarkOptionExplanation"
                explanation["member"] = []
                for cpt_pair in sample["question"]["choices"][i]["explanation"]:
                    pair = dict()
                    pair["@type"] = "QuestionAnswerConceptPair"
                    pair["questionConcept"] = cpt_pair["question_answer_concept_pair"][0]
                    pair["answerOptionConcept"] = cpt_pair["question_answer_concept_pair"][1]
                    pair["score"] = float(cpt_pair["pair_score"])
                    pair["path"] = []
                    for path in cpt_pair["paths"]:
                        cpt_rel_path = dict()
                        cpt_rel_path["@type"] = "QuestionAnswerConceptRelationPath"
                        cpt_rel_path["member"] = path["concept_relation_path"]
                        cpt_rel_path["score"] = float(path["path_score"])
                        pair["path"].append(cpt_rel_path)
                    explanation["member"].append(pair)
                choice["explanation"] = explanation
            choices.append(choice)
        return choices


if __name__ == "__main__":
    dataset = "CommonsenseQA"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = CommonsenseQA(question_set_id="train")
    benchmark.load_question_file("data/{}/train_rand_split.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/train_rand_split.jsonl".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_train.jsonl".format(dataset)))

    benchmark = CommonsenseQA(question_set_id="dev")
    benchmark.load_question_file("data/{}/dev_rand_split.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev_rand_split.jsonl".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset)))

    benchmark.load_question_file("data/{}/dev_rand_split_kagnet_submission.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev_rand_split_kagnet_submission.jsonl".format(dataset))
    benchmark.load_chosen_label_file("data/{}/dev_rand_split_kagnet_submission.jsonl".format(dataset))
    data = benchmark.convert_system_choices_to_jsonld("CommonsenseQA-kagnet")
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev_kagnet_submission.jsonl".format(dataset)))

    benchmark = CommonsenseQA(question_set_id="test")
    benchmark.load_question_file("data/{}/test_rand_split_no_answers.jsonl".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_test.jsonl".format(dataset)))

