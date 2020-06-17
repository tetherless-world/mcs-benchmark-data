
import json


class Benchmark(object):
    def load_question_file(self, path):
        raise NotImplementedError

    def load_label_file(self, path):
        raise NotImplementedError

    def get_benchmark_id(self):
        raise NotImplementedError

    def get_questions(self):
        raise NotImplementedError

    def get_question_type(self, question):
        raise NotImplementedError

    def get_question_categories(self, question):
        raise NotImplementedError

    def get_question_id(self, question):
        raise NotImplementedError

    def get_question_set_id(self, question):
        raise NotImplementedError

    def get_question_text(self, question):
        raise NotImplementedError

    def get_question_context(self, question):
        raise NotImplementedError

    def get_question_concept(self, question):
        raise NotImplementedError

    def get_choices(self, question):
        raise NotImplementedError

    def get_correct_choice_label(self, question):
        raise NotImplementedError

    def get_chosen_choice_label(self, question):
        raise NotImplementedError

    def convert(self):
        data = []

        for i, ques in enumerate(self.get_questions()):
            ques_data = dict()
            ques_data["benchmarkId"] = self.get_benchmark_id()
            ques_data["id"] = self.get_question_id(ques)
            ques_data["questionSetId"] = self.get_question_set_id(ques)
            ques_data["questionType"] = self.get_question_type(ques)
            ques_data["categories"] = self.get_question_categories(ques)
            ques_data["text"] = self.get_question_text(ques)
            ques_data["context"] = self.get_question_context(ques)
            ques_data["concept"] = self.get_question_concept(ques)
            ques_data["choices"] = self.get_choices(ques)
            ques_data["correctChoiceLabel"] = self.get_correct_choice_label(ques)
            ques_data["chosenChoiceLabel"] = self.get_chosen_choice_label(ques)
            data.append(ques_data)
        return data

    def write_data_as_jsonl(self, data, output_path):
        with open(output_path, "w") as f:
            for ques in data:
                f.write(json.dumps(ques))
                f.write("\n")

