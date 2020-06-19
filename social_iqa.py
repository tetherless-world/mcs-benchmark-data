
import os
import json

from benchmark import Benchmark


class SocialIQA(Benchmark):
    def __init__(self, question_set_id):
        super(SocialIQA, self).__init__()
        self.question_set_id = question_set_id
        self.benchmark_id = "SocialIQA"
        self.questions = []
        self.labels = dict()
        self.chosen_labels = dict()
        self.runid2guid = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                question = json.loads(line.strip())
                # Assign GUID if not provided
                question["guid"] = "{}-{}".format(self.question_set_id, i)
                self.questions.append(question)

    def load_label_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                label = line.strip()
                guid = "{}-{}".format(self.question_set_id, i)
                self.labels[guid] = label

    def load_chosen_label_file(self, path):
        pass

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_questions(self):
        return self.questions

    def get_question_type(self, question):
        return "multiple choice"

    def get_question_id(self, question):
        return question["guid"]

    def get_question_set_id(self, question):
        return self.question_set_id

    def get_question_text(self, question):
        return question["question"]

    def get_question_context(self, question):
        return question["context"]

    def get_correct_choice_label(self, question):
        return self.labels[self.get_question_id(question)]

    def get_chosen_choice_label(self, question):
        if self.get_question_id(question) not in self.chosen_labels:
            return ""
        return self.chosen_labels[self.get_question_id(question)]

    def get_choices(self, question):
        choices = []
        num_choices = 3
        choice_ids = ["A", "B", "C"]
        for i in range(num_choices):
            choices.append({
                "@type": "BenchmarkAnswer",
                "name": "Answer",
                "identifier": str(i + 1),
                "text": question["answer{}".format(choice_ids[i])]
            })
        return choices


if __name__ == "__main__":
    dataset = "SocialIQA"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = SocialIQA(question_set_id="train")
    benchmark.load_question_file("data/{}/train.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/train-labels.lst".format(dataset))
    data = benchmark.convert_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_train.jsonl".format(dataset)))

    benchmark = SocialIQA(question_set_id="dev")
    benchmark.load_question_file("data/{}/dev.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev-labels.lst".format(dataset))
    data = benchmark.convert_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset)))

