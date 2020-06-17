
import os
import json

from benchmark import Benchmark


class PhysicalIQA(Benchmark):
    def __init__(self, question_set_id):
        super(PhysicalIQA, self).__init__()

        self.question_set_id = question_set_id
        self.benchmark_id = "physicaliqa"
        self.questions = []
        self.labels = dict()
        self.chosen_labels = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                question = json.loads(line.strip())
                self.questions.append(question)

    def load_label_file(self, path):
        assert len(self.questions) > 0
        with open(path) as f:
            for i, line in enumerate(f):
                label = line.strip()
                self.labels[self.questions[i]["id"]] = label

    def load_chosen_label_file(self, path):
        pass

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_questions(self):
        return self.questions

    def get_question_type(self, question):
        return "multiple choice"

    def get_question_categories(self, question):
        return []

    def get_question_id(self, question):
        return question["id"]

    def get_question_set_id(self, question):
        return self.question_set_id

    def get_question_text(self, question):
        return question["goal"]

    def get_question_context(self, question):
        return ""

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
        num_choices = 2
        for i in range(num_choices):
            choices.append({
                "label": str(i),
                "text": question["sol{}".format(i + 1)]
            })
        return choices


if __name__ == "__main__":
    dataset = "PhysicalIQA"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = PhysicalIQA(question_set_id="train")
    benchmark.load_question_file("data/{}/train.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/train-labels.lst".format(dataset))
    data = benchmark.convert()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_train.jsonl".format(dataset)))

    benchmark = PhysicalIQA(question_set_id="dev")
    benchmark.load_question_file("data/{}/dev.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev-labels.lst".format(dataset))
    data = benchmark.convert()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset)))

