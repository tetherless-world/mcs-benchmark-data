
import os
import json
from benchmark import Benchmark


class CycIC(Benchmark):
    def __init__(self, question_set_id):
        super(CycIC, self).__init__()
        self.question_set_id = question_set_id
        self.benchmark_id = "CycIC"
        self.samples = []
        self.labels = dict()
        self.chosen_labels = dict()
        self.runid2guid = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for line in f:
                self.samples.append(json.loads(line.strip()))

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

    def get_samples(self):
        return self.samples

    def get_question_type(self, sample):
        return sample["questionType"]

    def get_question_categories(self, sample):
        return sample["categories"]

    def get_question_id(self, sample):
        return sample["guid"]

    def get_question_set_id(self, sample):
        return self.question_set_id

    def get_question_text(self, sample):
        return sample["question"]

    def get_correct_choice_label(self, sample):
        return self.labels[self.get_question_id(sample)]

    def get_chosen_choice_label(self, sample):
        if self.get_question_id(sample) not in self.chosen_labels:
            return ""
        return self.chosen_labels[self.get_question_id(sample)]

    def get_choices(self, sample):
        choices = []
        if self.get_question_type(sample) == "multiple choice":
            num_choices = 5
        elif self.get_question_type(sample) == "true/false":
            num_choices = 2

        for i in range(num_choices):
            choices.append({
                "@type": "BenchmarkAnswer",
                "name": "Answer",
                "identifier": str(i),
                "text": sample["answer_option{}".format(i)]
            })
        return choices


if __name__ == "__main__":
    dataset = "CycIC"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = CycIC(question_set_id="train")
    benchmark.load_question_file("data/CycIC/CycIC_training_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_training_labels.jsonl")
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_train.jsonl".format(dataset)))

    benchmark = CycIC(question_set_id="dev")
    benchmark.load_question_file("data/CycIC/CycIC_dev_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_dev_labels.jsonl")
    benchmark.load_chosen_label_file("data/CycIC/CycIC_dev_cycic-transformers_submission.jsonl")
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset)))
    data = benchmark.convert_system_choices_to_jsonld("CycIC-cycic-transformers")
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev_cycic-transformers_submission.jsonl".format(dataset)))

    benchmark = CycIC(question_set_id="test")
    benchmark.load_question_file("data/CycIC/CycIC_test_questions.jsonl")
    benchmark.load_label_file("data/CycIC/CycIC_test_labels.jsonl")
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_test.jsonl".format(dataset)))

