
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
        return None

    def get_question_id(self, question):
        raise NotImplementedError

    def get_question_set_id(self, question):
        raise NotImplementedError

    def get_question_text(self, question):
        return None

    def get_question_goal(self, question):
        return None

    def get_question_context(self, question):
        return None

    def get_question_concept(self, question):
        return None

    def get_choices(self, question):
        raise NotImplementedError

    def get_correct_choice_label(self, question):
        raise NotImplementedError

    def get_chosen_choice_label(self, question):
        raise NotImplementedError

    def convert_to_json(self):
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

    def convert_to_jsonld(self):
        data = []

        for i, ques in enumerate(self.get_questions()):
            ques_data = dict()
            ques_data["@id"] = self.get_benchmark_id() + "-" + self.get_question_id(ques)
            ques_data["@type"] = "BenchmarkSample"
            ques_data["inludedInDataset"] = self.get_benchmark_id() + "/" + self.get_question_set_id(ques)

            antecedents = list()
            category = dict()
            category["@type"] = "BenchmarkQuestionCategory"
            category["name"] = "Question category"
            category["text"] = self.get_question_categories(ques)
            if category["text"] is not None:
                antecedents.append(category)

            ques_type = dict()
            ques_type["@type"] = "BenchmarkQuestionType"
            ques_type["name"] = "Question type"
            ques_type["text"] = self.get_question_type(ques)
            if ques_type["text"] is not None:
                antecedents.append(ques_type)

            question = dict()
            question["@type"] = "BenchmarkQuestion"
            question["name"] = "Question"
            question["text"] = self.get_question_text(ques)
            if question["text"] is not None:
                antecedents.append(question)

            goal = dict()
            goal["@type"] = "BenchmarkGoal"
            goal["name"] = "Goal"
            goal["text"] = self.get_question_goal(ques)
            if goal["text"] is not None:
                antecedents.append(goal)

            context = dict()
            context["@type"] = "BenchmarkContext"
            context["name"] = "Context"
            context["text"] = self.get_question_context(ques)
            if context["text"] is not None:
                antecedents.append(context)

            concept = dict()
            concept["@type"] = "BenchmarkQuestionConcept"
            concept["name"] = "Question concept"
            concept["text"] = self.get_question_concept(ques)
            if concept["text"] is not None:
                antecedents.append(concept)

            ques_data["antecedent"] = dict()
            ques_data["antecedent"]["@type"] = "BenchmarkSampleAntecedent"
            ques_data["antecedent"]["numberOfItems"] = len(antecedents)
            for pos in range(len(antecedents)):
                antecedents[pos]["position"] = pos
            ques_data["antecedent"]["itemListElement"] = antecedents

            choices = self.get_choices(ques)
            ques_data["choice"] = dict()
            ques_data["choice"]["@type"] = "BenchmarkChoice"
            ques_data["choice"]["numberOfItems"] = len(choices)
            for pos in range(len(choices)):
                choices[pos]["position"] = pos
            ques_data["choice"]["itemListElement"] = choices
            ques_data["correctChoice"] = self.get_correct_choice_label(ques)
            ques_data["chosenChoiceLabel"] = self.get_chosen_choice_label(ques)
            data.append(ques_data)
        return data

    def write_data_as_jsonl(self, data, output_path):
        with open(output_path, "w") as f:
            for ques in data:
                f.write(json.dumps(ques))
                f.write("\n")

