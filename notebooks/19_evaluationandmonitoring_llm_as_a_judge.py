import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import google.generativeai as genai
    import os
    import json
    import logging
    from typing import Optional

    # --- Configuration ---
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set your API key as an environment variable to run this script
    # For example, in your terminal: export GOOGLE_API_KEY='your_key_here'
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        logging.error("Error: GOOGLE_API_KEY environment variable not set.")
        exit(1)

    # --- LLM-as-a-Judge Rubric for Legal Survey Quality ---
    LEGAL_SURVEY_RUBRIC = """
    You are an expert legal survey methodologist and a critical legal reviewer. Your task is to evaluate the quality of a given legal survey question.

    Provide a score from 1 to 5 for overall quality, along with a detailed rationale and specific feedback.
    Focus on the following criteria:

    1.  **Clarity & Precision (Score 1-5):**
        * 1: Extremely vague, highly ambiguous, or confusing.
        * 3: Moderately clear, but could be more precise.
        * 5: Perfectly clear, unambiguous, and precise in its legal terminology (if applicable) and intent.

    2.  **Neutrality & Bias (Score 1-5):**
        * 1: Highly leading or biased, clearly influencing the respondent towards a specific answer.
        * 3: Slightly suggestive or could be interpreted as leading.
        * 5: Completely neutral, objective, and free from any leading language or loaded terms.

    3.  **Relevance & Focus (Score 1-5):**
        * 1: Irrelevant to the stated survey topic or out of scope.
        * 3: Loosely related but could be more focused.
        * 5: Directly relevant to the survey's objectives and well-focused on a single concept.

    4.  **Completeness (Score 1-5):**
        * 1: Omits critical information needed to answer accurately or provides insufficient context.
        * 3: Mostly complete, but minor details are missing.
        * 5: Provides all necessary context and information for the respondent to answer thoroughly.

    5.  **Appropriateness for Audience (Score 1-5):**
        * 1: Uses jargon inaccessible to the target audience or is overly simplistic for experts.
        * 3: Generally appropriate, but some terms might be challenging or oversimplified.
        * 5: Perfectly tailored to the assumed legal knowledge and background of the target survey audience.

    **Output Format:**
    Your response MUST be a JSON object with the following keys:
    * `overall_score`: An integer from 1 to 5 (average of criterion scores, or your holistic judgment).
    * `rationale`: A concise summary of why this score was given, highlighting major strengths and weaknesses.
    * `detailed_feedback`: A bullet-point list detailing feedback for each criterion (Clarity, Neutrality, Relevance, Completeness, Audience Appropriateness). Suggest specific improvements.
    * `concerns`: A list of any specific legal, ethical, or methodological concerns.
    * `recommended_action`: A brief recommendation (e.g., "Revise for neutrality", "Approve as is", "Clarify scope").
    """

    class LLMJudgeForLegalSurvey:
        """A class to evaluate legal survey questions using a generative AI model."""

        def __init__(self, model_name: str = 'gemini-1.5-flash-latest', temperature: float = 0.2):
            """
            Initializes the LLM Judge.

            Args:
                model_name (str): The name of the Gemini model to use.
                                  'gemini-1.5-flash-latest' is recommended for speed and cost.
                                  'gemini-1.5-pro-latest' offers the highest quality.
                temperature (float): The generation temperature. Lower is better for deterministic evaluation.
            """
            self.model = genai.GenerativeModel(model_name)
            self.temperature = temperature

        def _generate_prompt(self, survey_question: str) -> str:
            """Constructs the full prompt for the LLM judge."""
            return f"{LEGAL_SURVEY_RUBRIC}\n\n---\n**LEGAL SURVEY QUESTION TO EVALUATE:**\n{survey_question}\n---"

        def judge_survey_question(self, survey_question: str) -> Optional[dict]:
            """
            Judges the quality of a single legal survey question using the LLM.

            Args:
                survey_question (str): The legal survey question to be evaluated.

            Returns:
                Optional[dict]: A dictionary containing the LLM's judgment, or None if an error occurs.
            """
            full_prompt = self._generate_prompt(survey_question)

            try:
                logging.info(f"Sending request to '{self.model.model_name}' for judgment...")
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                        response_mime_type="application/json"
                    )
                )

                # Check for content moderation or other reasons for an empty response.
                if not response.parts:
                    safety_ratings = response.prompt_feedback.safety_ratings
                    logging.error(f"LLM response was empty or blocked. Safety Ratings: {safety_ratings}")
                    return None

                return json.loads(response.text)

            except json.JSONDecodeError:
                logging.error(f"Failed to decode LLM response as JSON. Raw response: {response.text}")
                return None
            except Exception as e:
                logging.error(f"An unexpected error occurred during LLM judgment: {e}")
                return None

    # --- Example Usage ---
    if __name__ == "__main__":
        judge = LLMJudgeForLegalSurvey()

        # --- Good Example ---
        good_legal_survey_question = """
        To what extent do you agree or disagree that current intellectual property laws in Switzerland adequately protect emerging AI-generated content, assuming the content meets the originality criteria established by the Federal Supreme Court?
        (Select one: Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree)
        """
        print("\n--- Evaluating Good Legal Survey Question ---")
        judgment_good = judge.judge_survey_question(good_legal_survey_question)
        if judgment_good:
            print(json.dumps(judgment_good, indent=2))

        # --- Biased/Poor Example ---
        biased_legal_survey_question = """
        Don't you agree that overly restrictive data privacy laws like the FADP are hindering essential technological innovation and economic growth in Switzerland?
        (Select one: Yes, No)
        """
        print("\n--- Evaluating Biased Legal Survey Question ---")
        judgment_biased = judge.judge_survey_question(biased_legal_survey_question)
        if judgment_biased:
            print(json.dumps(judgment_biased, indent=2))

        # --- Ambiguous/Vague Example ---
        vague_legal_survey_question = """
        What are your thoughts on legal tech?
        """
        print("\n--- Evaluating Vague Legal Survey Question ---")
        judgment_vague = judge.judge_survey_question(vague_legal_survey_question)
        if judgment_vague:
            print(json.dumps(judgment_vague, indent=2))
    return


if __name__ == "__main__":
    app.run()
