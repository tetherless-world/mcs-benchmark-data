
import json


class Benchmark(object):
    def load_question_file(self, path):
        raise NotImplementedError

    def load_label_file(self, path):
        raise NotImplementedError

    def get_benchmark_id(self):
        raise NotImplementedError

    def get_samples(self):
        raise NotImplementedError

    def get_question_type(self, sample):
        raise NotImplementedError

    def get_question_categories(self, sample):
        return None

    def get_question_id(self, sample):
        raise NotImplementedError

    def get_question_set_id(self, sample):
        raise NotImplementedError

    def get_question_text(self, sample):
        return None

    def get_question_observation(self, sample):
        return None

    def get_question_goal(self, sample):
        return None

    def get_question_context(self, sample):
        return None

    def get_question_concept(self, sample):
        return None

    def get_choices(self, sample):
        raise NotImplementedError

    def get_choice_explanation(self, sample):
        return None

    def get_correct_choice(self, sample):
        raise NotImplementedError

    def get_chosen_choice(self, sample):
        raise NotImplementedError

    def has_explanation(self):
        return False

    def convert_to_json(self):
        data = []

        for i, spl in enumerate(self.get_questions()):
            spl_data = dict()
            spl_data["benchmarkId"] = self.get_benchmark_id()
            spl_data["id"] = self.get_question_id(spl)
            spl_data["questionSetId"] = self.get_question_set_id(spl)
            spl_data["questionType"] = self.get_question_type(spl)
            spl_data["categories"] = self.get_question_categories(spl)
            spl_data["text"] = self.get_question_text(spl)
            spl_data["context"] = self.get_question_context(spl)
            spl_data["concept"] = self.get_question_concept(spl)
            spl_data["choices"] = self.get_choices(spl)
            spl_data["correctChoice"] = self.get_correct_choice(spl)
            spl_data["chosenChoice"] = self.get_chosen_choice(spl)
            data.append(spl_data)
        return data

    def convert_samples_to_jsonld(self):
        data = []

        for i, spl in enumerate(self.get_samples()):
            spl_data = dict()
            spl_data["@context"] = "http://schema.org/"
            spl_data["@id"] = self.get_benchmark_id() + "-" + self.get_question_id(spl)
            spl_data["@type"] = "BenchmarkSample"
            spl_data["includedInDataset"] = self.get_benchmark_id() + "/" + self.get_question_set_id(spl)

            antecedents = list()
            category = dict()
            category["@type"] = "BenchmarkQuestionCategory"
            category["name"] = "Question category"
            category["text"] = self.get_question_categories(spl)
            if category["text"] is not None:
                antecedents.append(category)

            ques_type = dict()
            ques_type["@type"] = "BenchmarkQuestionType"
            ques_type["name"] = "Question type"
            ques_type["text"] = self.get_question_type(spl)
            if ques_type["text"] is not None:
                antecedents.append(ques_type)

            question = dict()
            question["@type"] = "BenchmarkQuestion"
            question["name"] = "Question"
            question["text"] = self.get_question_text(spl)
            if question["text"] is not None:
                antecedents.append(question)

            observations = self.get_question_observation(spl)
            if observations is not None:
                for obs in observations:
                    antecedents.append(obs)

            goal = dict()
            goal["@type"] = "BenchmarkGoal"
            goal["name"] = "Goal"
            goal["text"] = self.get_question_goal(spl)
            if goal["text"] is not None:
                antecedents.append(goal)

            context = dict()
            context["@type"] = "BenchmarkContext"
            context["name"] = "Context"
            context["text"] = self.get_question_context(spl)
            if context["text"] is not None:
                antecedents.append(context)

            concept = dict()
            concept["@type"] = "BenchmarkQuestionConcept"
            concept["name"] = "Question concept"
            concept["text"] = self.get_question_concept(spl)
            if concept["text"] is not None:
                antecedents.append(concept)

            spl_data["antecedent"] = dict()
            spl_data["antecedent"]["@type"] = "BenchmarkSampleAntecedent"
            spl_data["antecedent"]["numberOfItems"] = len(antecedents)
            for pos in range(len(antecedents)):
                antecedents[pos]["position"] = pos
            spl_data["antecedent"]["itemListElement"] = antecedents

            choices = self.get_choices(spl)
            spl_data["choices"] = dict()
            spl_data["choices"]["@type"] = "BenchmarkChoices"
            spl_data["choices"]["numberOfItems"] = len(choices)
            for pos in range(len(choices)):
                choices[pos]["position"] = pos
                choices[pos]["@id"] = "{}-{}".format(spl_data["@id"], pos)
            spl_data["choices"]["itemListElement"] = choices
            spl_data["correctChoice"] = "{}-{}".format(spl_data["@id"], self.get_correct_choice(spl))
            data.append(spl_data)
        return data

    def convert_system_choices_to_jsonld(self, submission_id):
        data = []
        for i, spl in enumerate(self.get_samples()):
            spl_data = dict()
            spl_data["@context"] = "http://schema.org/"
            spl_data["@type"] = "SubmissionSample"
            spl_data["about"] = self.get_benchmark_id() + "-" + self.get_question_id(spl)
            spl_data["includedInDataset"] = submission_id
            if self.has_explanation():
                explanation = self.get_choice_explanation(spl)
                if explanation is not None:
                    spl_data["explanation"] = explanation
            spl_data["value"] = "{}-{}".format(spl_data["about"], self.get_chosen_choice(spl))
            data.append(spl_data)
        return data

    def write_data_as_jsonl(self, data, output_path):
        with open(output_path, "w") as f:
            for sample in data:
                f.write(json.dumps(sample))
                f.write("\n")

