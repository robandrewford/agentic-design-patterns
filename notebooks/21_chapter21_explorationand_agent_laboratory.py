import marimo

__generated_with = "0.18.4"
app = marimo.App()


app._unparsable_cell(
    r"""
    # as seen in https://github.com/SamuelSchmidgall/AgentLaboratory/blob/main/agents.py

    class ReviewersAgent:
        def __init__(self, model=\"gpt-4o-mini\", notes=None, openai_api_key=None):
            if notes is None: self.notes = []
            else: self.notes = notes
            self.model = model
            self.openai_api_key = openai_api_key

        def inference(self, plan, report):
            reviewer_1 = \"You are a harsh but fair reviewer and expect good experiments that lead to insights for the research topic.\"
            review_1 = get_score(outlined_plan=plan, latex=report, reward_model_llm=self.model, reviewer_type=reviewer_1, openai_api_key=self.openai_api_key)

            reviewer_2 = \"You are a harsh and critical but fair reviewer who is looking for an idea that would be impactful in the field.\"
            review_2 = get_score(outlined_plan=plan, latex=report, reward_model_llm=self.model, reviewer_type=reviewer_2, openai_api_key=self.openai_api_key)

            reviewer_3 = \"You are a harsh but fair open-minded reviewer that is looking for novel ideas that have not been proposed before.\"
            review_3 = get_score(outlined_plan=plan, latex=report, reward_model_llm=self.model, reviewer_type=reviewer_3, openai_api_key=self.openai_api_key)

            return f\"Reviewer #1:\n{review_1}, \nReviewer #2:\n{review_2}, \nReviewer #3:\n{review_3}\"


    #
    def get_score(outlined_plan, latex, reward_model_llm, reviewer_type=None, attempts=3, openai_api_key=None):
        e = str()
        for _attempt in range(attempts):
            try:
                # todo: have a reward function here
                # template inherited from the AI Scientist (good work on this prompt Sakana AI team :D)
                template_instructions = \"\"\"
                Respond in the following format:

                THOUGHT:
                <THOUGHT>

                REVIEW JSON:
                ```json
                <JSON>
                ```

                In <THOUGHT>, first briefly discuss your intuitions and reasoning for the evaluation.
                Detail your high-level arguments, necessary choices and desired outcomes of the review.
                Do not make generic comments here, but be specific to your current paper.
                Treat this as the note-taking phase of your review.

                In <JSON>, provide the review in JSON format with the following fields in the order:
                - \"Summary\": A summary of the paper content and its contributions.
                - \"Strengths\": A list of strengths of the paper.
                - \"Weaknesses\": A list of weaknesses of the paper.
                - \"Originality\": A rating from 1 to 4 (low, medium, high, very high).
                - \"Quality\": A rating from 1 to 4 (low, medium, high, very high).
                - \"Clarity\": A rating from 1 to 4 (low, medium, high, very high).
                - \"Significance\": A rating from 1 to 4 (low, medium, high, very high).
                - \"Questions\": A set of clarifying questions to be answered by the paper authors.
                - \"Limitations\": A set of limitations and potential negative societal impacts of the work.
                - \"Ethical Concerns\": A boolean value indicating whether there are ethical concerns.
                - \"Soundness\": A rating from 1 to 4 (poor, fair, good, excellent).
                - \"Presentation\": A rating from 1 to 4 (poor, fair, good, excellent).
                - \"Contribution\": A rating from 1 to 4 (poor, fair, good, excellent).
                - \"Overall\": A rating from 1 to 10 (very strong reject to award quality).
                - \"Confidence\": A rating from 1 to 5 (low, medium, high, very high, absolute).
                - \"Decision\": A decision that has to be one of the following: Accept, Reject.

                For the \"Decision\" field, don't use Weak Accept, Borderline Accept, Borderline Reject, or Strong Reject. Instead, only use Accept or Reject.
                This JSON will be automatically parsed, so ensure the format is precise.
                \"\"\"

    class ProfessorAgent(BaseAgent):
        def __init__(self, model=\"gpt4omini\", notes=None, max_steps=100, openai_api_key=None):
            super().__init__(model, notes, max_steps, openai_api_key)
            self.phases = [\"report writing\"]

        def generate_readme(self):
            sys_prompt = f\"\"\"You are {self.role_description()} \n Here is the written paper \n{self.report}. Task instructions: Your goal is to integrate all of the knowledge, code, reports, and notes provided to you and generate a readme.md for a github repository.\"\"\"
            history_str = \"\n\".join([_[1] for _ in self.history])
            prompt = (
                f\"\"\"History: {history_str}\n{'~' * 10}\n\"\"\"
                f\"Please produce the readme below in markdown:\n\")
            model_resp = query_model(model_str=self.model, system_prompt=sys_prompt, prompt=prompt, openai_api_key=self.openai_api_key)
            return model_resp.replace(\"```markdown\", \"\")


    class PostdocAgent(BaseAgent):
        def __init__(self, model=\"gpt4omini\", notes=None, max_steps=100, openai_api_key=None):
            super().__init__(model, notes, max_steps, openai_api_key)
            self.phases = [\"plan formulation\", \"results interpretation\"]

        def context(self, phase):
            sr_str = str()
            if self.second_round:
                sr_str = (
                    f\"The following are results from the previous experiments\n\",
                    f\"Previous Experiment code: {self.prev_results_code}\n\"
                    f\"Previous Results: {self.prev_exp_results}\n\"
                    f\"Previous Interpretation of results: {self.prev_interpretation}\n\"
                    f\"Previous Report: {self.prev_report}\n\"
                    f\"{self.reviewer_response}\n\n\n\"
                )
            if phase == \"plan formulation\":
                return (
                    sr_str,
                    f\"Current Literature Review: {self.lit_review_sum}\",
                )
            elif phase == \"results interpretation\":
                return (
                    sr_str,
                    f\"Current Literature Review: {self.lit_review_sum}\n\"
                    f\"Current Plan: {self.plan}\n\"
                    f\"Current Dataset code: {self.dataset_code}\n\"
                    f\"Current Experiment code: {self.results_code}\n\"
                    f\"Current Results: {self.exp_results}\"
                )
            return \"\"

    #
    #
    \"You are a machine learning engineer being directed by a PhD student who will help you write the code, and you can interact with them through dialogue.\n\"
    \"Your goal is to produce code that prepares the data for the provided experiment. You should aim for simple code to prepare the data, not complex code. You should integrate the provided literature review and the plan and come up with code to prepare data for this experiment.\n\"

    #
    #
    \"You are a software engineer directing a machine learning engineer, where the machine learning engineer will be writing the code, and you can interact with them through dialogue.\n\"
    \"Your goal is to help the ML engineer produce code that prepares the data for the provided experiment. You should aim for very simple code to prepare the data, not complex code. You should integrate the provided literature review and the plan and come up with code to prepare data for this experiment.\n\"
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
