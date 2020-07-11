
import os
import json

from benchmark import Benchmark


class ANLI(Benchmark):
    def __init__(self, question_set_id):
        super(ANLI, self).__init__()

        self.question_set_id = question_set_id
        self.benchmark_id = "ANLI"
        self.samples = []
        self.labels = dict()
        self.chosen_labels = dict()

    def load_question_file(self, path):
        with open(path) as f:
            for i, line in enumerate(f):
                sample = json.loads(line.strip())
                self.samples.append(sample)

    def load_label_file(self, path):
        assert len(self.samples) > 0
        with open(path) as f:
            for i, line in enumerate(f):
                if len(line.strip()) == 0:
                    continue
                label = int(line.strip()) - 1
                self.labels[self.get_question_id(self.samples[i])] = label

    def load_chosen_label_file(self, path):
        pass

    def get_benchmark_id(self):
        return self.benchmark_id

    def get_samples(self):
        return self.samples

    def get_question_type(self, sample):
        return "multiple choice"

    def get_question_id(self, sample):
        return sample["story_id"]

    def get_question_set_id(self, sample):
        return self.question_set_id

    def get_question_observation(self, sample):
        observations = []
        num_obs = 2
        for i in range(num_obs):
            observations.append({
                "@type": "BenchmarkObservation",
                "name": "Observation",
                "text": sample["obs{}".format(i + 1)]
            })
        return observations

    def get_correct_choice(self, sample):
        return self.labels[self.get_question_id(sample)]

    def get_chosen_choice(self, sample):
        if self.get_question_id(sample) not in self.chosen_labels:
            return None
        return self.chosen_labels[self.get_question_id(sample)]

    def get_choices(self, sample):
        choices = []
        num_choices = 2
        for i in range(num_choices):
            choices.append({
                "@type": "BenchmarkHypothesis",
                "name": "Hypothesis",
                "text": sample["hyp{}".format(i + 1)]
            })
        return choices


if __name__ == "__main__":
    dataset = "ANLI"
    output_dir = "converted/{}".format(dataset)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    benchmark = ANLI(question_set_id="train")
    benchmark.load_question_file("data/{}/train.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/train-labels.lst".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_train.jsonl".format(dataset)))

    benchmark = ANLI(question_set_id="dev")
    benchmark.load_question_file("data/{}/dev.jsonl".format(dataset))
    benchmark.load_label_file("data/{}/dev-labels.lst".format(dataset))
    data = benchmark.convert_samples_to_jsonld()
    benchmark.write_data_as_jsonl(data, os.path.join(output_dir, "{}_dev.jsonl".format(dataset)))

