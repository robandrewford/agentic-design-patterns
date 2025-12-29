import marimo

__generated_with = "0.18.4"
app = marimo.App()


app._unparsable_cell(
    r"""
    You are an Information Retrieval Agent. Your goal is to answer the user's question comprehensively and accurately by thinking step-by-step.

    Here's the process you must follow:

    1.  **Analyze the Query:** Understand the core subject and specific requirements of the user's question. Identify key entities, keywords, and the type of information being sought.
    2.  **Formulate Search Queries (for Knowledge Base):** Based on your analysis, generate a list of precise search queries that you would use to retrieve relevant information from a knowledge base or external tools.
    3.  **Simulate Information Retrieval (Self-Correction/Reasoning):** For each search query, mentally consider what kind of information you expect to find. If you were to retrieve the content, what would be the most relevant snippets? Think about potential ambiguities or missing pieces.
    4.  **Synthesize Information:** Based on the simulated retrieval and your understanding of the user's original query, synthesize the gathered information into a coherent and complete answer. Ensure all aspects of the query are addressed.
    5.  **Review and Refine:** Before finalizing, critically evaluate your answer. Is it accurate? Is it comprehensive? Is it easy to understand? Is it concise? If not, identify what needs to be improved and how.

    **User Query:** \"Explain the main differences between classical computers and quantum computers, and briefly describe a potential application of quantum computing.\"

    **Agent's Thought Process (Internal CoT Output - encouraged by the prompt):**

    **Thought 1 (Analyze Query):**
    The user wants two things:
    1.  Main differences between classical and quantum computers.
    2.  One potential application of quantum computing.
    Keywords: classical computers, quantum computers, differences, potential application.

    **Thought 2 (Formulate Search Queries):**
    - \"differences classical vs quantum computers\"
    - \"how quantum computers work\"
    - \"how classical computers work\"
    - \"applications of quantum computing\"

    **Thought 3 (Simulate Information Retrieval & Identify Key Concepts):**
    - From \"differences\": Expect concepts like bits vs. qubits, superposition, entanglement, probabilistic nature, computational power for specific problems.
    - From \"how they work\": Classical uses transistors/binary. Quantum uses quantum mechanics.
    - From \"applications\": Expect drug discovery, material science, cryptography, optimization.

    **Thought 4 (Synthesize Information):**
    Classical computers use bits (0 or 1), processing information sequentially. Quantum computers use qubits, which can be 0, 1, or both simultaneously (superposition), and can be entangled, allowing for vastly different computational approaches. This enables them to solve certain problems (like factoring large numbers or simulating complex molecules) far more efficiently than classical computers. A potential application is in drug discovery, where quantum computers could simulate molecular interactions with unprecedented accuracy, accelerating the development of new medicines.

    **Thought 5 (Review and Refine):**
    - Differences are covered (bits vs qubits, superposition, entanglement, processing).
    - Application is given (drug discovery).
    - Is it brief? Yes.
    - Is it clear? Yes.
    - Looks good.

    **Agent's Final Answer (Output to User):**

    Classical computers process information using bits, which can be either a 0 or a 1 at any given time, performing operations sequentially. In contrast, quantum computers utilize qubits, which can exist in multiple states simultaneously through superposition and can be linked through entanglement, allowing for exponentially more complex computations. This fundamental difference enables quantum machines to tackle certain problems, such as simulating molecular structures or breaking complex encryption, that are intractable for even the most powerful classical supercomputers. A significant potential application of quantum computing lies in drug discovery, where its ability to precisely model molecular behavior could revolutionize the development of new pharmaceuticals.
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
