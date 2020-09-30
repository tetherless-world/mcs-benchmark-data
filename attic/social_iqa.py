import os
import json

from benchmark import Benchmark


class SocialIQA(Benchmark):
    def __init__(self, question_set_id):
        super(SocialIQA, self).__init__()
        self.question_set_id = question_set_id
        self.benchmark_id = "SocialIQA"
        self.samples = []
        self.labels = dict()
        self.chosen_labels = dict()
        self.runid2guid = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                if len(line.strip()) == 0:
                    continue
                sample = json.loads(line.strip())
                # Assign GUID if not provided
                sample["guid"] = "{}-{}".format(self.question_set_id, i)
                self.samples.append(sample)

    def load_label_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                if len(line.strip()) == 0:
                    continue
                label = int(line.strip()) - 1  # zero-based
                guid = "{}-{}".format(self.question_set_id, i)
                self.labels[guid] = label

    def load_chosen_label_file(self, path):
        pass

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_samples(self):
        return self.samples

    def get_question_type(self, sample):
        return "multiple choice"

    def get_question_id(self, sample):
        return sample["guid"]

    def get_question_set_id(self, sample):
        return self.question_set_id

    def get_question_text(self, sample):
        return sample["question"]

    def get_question_context(self, sample):
        return sample["context"]

    def get_correct_choice(self, sample):
        return self.labels[self.get_question_id(sample)]

    def get_chosen_choice(self, sample):
        if self.get_question_id(sample) not in self.chosen_labels:
            return None
        return self.chosen_labels[self.get_question_id(sample)]

    def get_choices(self, sample):
        choices = []
        num_choices = 3
        choice_ids = ["A", "B", "C"]
        for i in range(num_choices):
            choices.append(
                {
                    "@type": "BenchmarkAnswer",
                    "name": "Answer",
                    "text": sample["answer{}".format(choice_ids[i])],
                }
            )
        return choices


if __name__ == "__main__":
    dataset = "SocialIQA"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = SocialIQA(question_set_id="train")
    benchmark.load_question_file("data/{}/train.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/train-labels.lst".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(
        data, os.path.join(output_dir, "{}_train.jsonl".format(dataset))
    )

    benchmark = SocialIQA(question_set_id="dev")
    benchmark.load_question_file("data/{}/dev.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev-labels.lst".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(
        data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset))
    )
