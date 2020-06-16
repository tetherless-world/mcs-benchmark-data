
import os
import json
from benchmark import Benchmark


class CycIC(Benchmark):
    def __init__(self, question_set_id):
        super(CycIC, self).__init__()
        self.question_set_id = question_set_id
        self.benchmark_id = "cycic"
        self.questions = []
        self.labels = dict()
        self.chosen_labels = dict()
        self.runid2guid = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for line in f:
                self.questions.append(json.loads(line.strip()))

    def load_label_file(self, path):
        with open(path) as f:
            for line in f:
                json_data = json.loads(line.strip())
                self.labels[json_data["guid"]] = str(json_data["correct_answer"])
                self.runid2guid[json_data["run_id"]] = json_data["guid"]

    def load_chosen_label_file(self, path):
        with open(path) as f:
            for line in f:
                json_data = json.loads(line.strip())
                self.chosen_labels[self.runid2guid[json_data["example_id"]]] = json_data["pred"]

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_questions(self):
        return self.questions

    def get_question_type(self, question):
        return question["questionType"]

    def get_question_categories(self, question):
        return question["categories"]

    def get_question_id(self, question):
        return question["guid"]

    def get_question_set_id(self, question):
        return self.question_set_id

    def get_question_text(self, question):
        return question["question"]

    def get_question_concept(self, question):
        return ""

    def get_correct_choice_label(self, question):
        return self.labels[self.get_question_id(question)]

    def get_chosen_choice_label(self, question):
        if self.get_question_id(question) not in self.chosen_labels:
            return ""
        return self.chosen_labels[self.get_question_id(question)]

    def get_choices(self, question):
        choices = []
        if self.get_question_type(question) == "multiple choice":
            num_choices = 5
        elif self.get_question_type(question) == "true/false":
            num_choices = 2

        for i in range(num_choices):
            choices.append({
                "label": str(i),
                "text": question["answer_option{}".format(i)]
            })
        return choices


if __name__ == "__main__":
    output_dir = "converted/CycIC"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = CycIC(question_set_id="train")
    benchmark.load_question_file("data/CycIC/CycIC_training_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_training_labels.jsonl")
    data = benchmark.convert()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "CycIC_train.jsonl"))

    benchmark = CycIC(question_set_id="dev")
    benchmark.load_question_file("data/CycIC/CycIC_dev_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_dev_labels.jsonl")
    benchmark.load_chosen_label_file("data/CycIC/CycIC_dev_predictions.jsonl")
    data = benchmark.convert()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "CycIC_dev.jsonl"))

    benchmark = CycIC(question_set_id="test")
    benchmark.load_question_file("data/CycIC/CycIC_test_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_test_labels.jsonl")
    data = benchmark.convert()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "CycIC_test.jsonl"))

