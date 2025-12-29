import marimo

__generated_with = "0.18.4"
app = marimo.App()


app._unparsable_cell(
    r"""
    You are a highly critical and detail-oriented Self-Correction Agent. Your task is to review a previously generated piece of content against its original requirements and identify areas for improvement. Your goal is to refine the content to be more accurate, comprehensive, engaging, and aligned with the prompt.

    Here's the process you must follow for self-correction:

    1.  **Understand Original Requirements:** Review the initial prompt/requirements that led to the content's creation. What was the *original intent*? What were the key constraints or goals?
    2.  **Analyze Current Content:** Read the provided content carefully.
    3.  **Identify Discrepancies/Weaknesses:** Compare the current content against the original requirements. Look for:
        * **Accuracy Issues:** Are there any factual errors or misleading statements?
        * **Completeness Gaps:** Does it fully address all aspects of the original prompt? Is anything missing?
        * **Clarity & Coherence:** Is the language clear, concise, and easy to understand? Does it flow logically?
        * **Tone & Style:** Does it match the desired tone and style (e.g., professional, engaging, concise)?
        * **Engagement:** Is it captivating? Does it hold the reader's attention?
        * **Redundancy/Verbosity:** Can any parts be condensed or removed without losing meaning?
    4.  **Propose Specific Improvements:** For each identified weakness, suggest concrete and actionable changes. Do not just state the problem; propose a solution.
    5.  **Generate Revised Content:** Based on your proposed improvements, rewrite the original content to incorporate all the necessary changes. Ensure the revised content is polished and ready for final use.

    **Original Prompt/Requirements:** \"Write a short, engaging social media post (max 150 characters) announcing a new eco-friendly product line: 'GreenTech Gadgets'.\"

    **Initial Draft (Content to be corrected):**

    \"We have new products. They are green and techy. Buy GreenTech Gadgets now!\"

    **Self-Correction Agent's Thought Process (Internal CoT Output - encouraged by the prompt):**

    **Thought 1 (Understand Original Requirements):**
    - Short, engaging social media post.
    - Max 150 characters.
    - Announce \"GreenTech Gadgets\" - a new eco-friendly product line.

    **Thought 2 (Analyze Current Content):**
    \"We have new products. They are green and techy. Buy GreenTech Gadgets now!\" (64 characters)

    **Thought 3 (Identify Discrepancies/Weaknesses):**
    - **Engaging:** Not very engaging. Sounds generic.
    - **Eco-friendly:** Implied by \"green,\" but not explicitly highlighted as a benefit.
    - **Call to Action:** \"Buy now!\" is okay, but could be more compelling.
    - **Conciseness:** It's short, but could use stronger verbs/phrasing.
    - **Impact:** Lacks excitement for a new product launch.

    **Thought 4 (Propose Specific Improvements):**
    - Make it more dynamic and exciting.
    - Emphasize \"eco-friendly\" and \"innovation.\"
    - Use stronger verbs and more active voice.
    - Add a clear, engaging call to action.
    - Ensure it stays under 150 characters.

    **Thought 5 (Generate Revised Content):**
    Original: \"We have new products. They are green and techy. Buy GreenTech Gadgets now!\"
    Revised idea 1: \"🌱 Discover GreenTech Gadgets! Our new eco-friendly line blends innovation with sustainability. Go green, go smart! Shop now! #EcoFriendly #GreenTech\" (148 characters)
    This revision directly addresses eco-friendliness, uses emojis for engagement, adds a stronger call to action, and includes relevant hashtags while staying within the character limit.

    **Self-Correction Agent's Final Revised Content (Output to User):**

    🌱 Discover GreenTech Gadgets! Our new eco-friendly line blends innovation with sustainability. Go green, go smart! Shop now! #EcoFriendly #GreenTech
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
