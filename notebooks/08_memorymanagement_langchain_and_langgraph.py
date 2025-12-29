import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    from langchain.memory import ChatMessageHistory

    # Initialize the history object
    history = ChatMessageHistory()

    # Add user and AI messages
    history.add_user_message("I'm heading to New York next week.")
    history.add_ai_message("Great! It's a fantastic city.")

    # Access the list of messages
    print(history.messages)
    return


@app.cell
def _():
    from langchain.memory import ConversationBufferMemory
    _memory = ConversationBufferMemory()
    # Initialize memory
    _memory.save_context({'input': "What's the weather like?"}, {'output': "It's sunny today."})
    # Save a conversation turn
    # Load the memory as a string
    print(_memory.load_memory_variables({}))
    return (ConversationBufferMemory,)


@app.cell
def _(ConversationBufferMemory):
    from langchain_openai import OpenAI
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    llm = OpenAI(temperature=0)
    template = 'You are a helpful travel agent.\n\nPrevious conversation:\n{history}\n\nNew question: {question}\nResponse:'
    _prompt = PromptTemplate.from_template(template)
    _memory = ConversationBufferMemory(memory_key='history')
    _conversation = LLMChain(llm=llm, prompt=_prompt, memory=_memory)
    _response = _conversation.predict(question='I want to book a flight.')
    print(_response)
    _response = _conversation.predict(question='My name is Sam, by the way.')
    print(_response)
    _response = _conversation.predict(question='What was my name again?')
    print(_response)
    return (LLMChain,)


@app.cell
def _(ConversationBufferMemory, LLMChain):
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    llm_1 = ChatOpenAI()
    _prompt = ChatPromptTemplate(messages=[SystemMessagePromptTemplate.from_template('You are a friendly assistant.'), MessagesPlaceholder(variable_name='chat_history'), HumanMessagePromptTemplate.from_template('{question}')])
    _memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    _conversation = LLMChain(llm=llm_1, prompt=_prompt, memory=_memory)
    _response = _conversation.predict(question="Hi, I'm Jane.")
    print(_response)
    _response = _conversation.predict(question='Do you remember my name?')
    print(_response)
    return (llm_1,)


@app.cell
def _(BaseStore, State, llm_1, prompt_template):
    def update_instructions(state: State, store: BaseStore):
        namespace = ('instructions',)
        current_instructions = store.search(namespace)[0]
        _prompt = prompt_template.format(instructions=current_instructions.value['instructions'], conversation=state['messages'])
        output = llm_1.invoke(_prompt)
        new_instructions = output['new_instructions']
        store.put(('agent_instructions',), 'agent_a', {'instructions': new_instructions})

    def call_model(state: State, store: BaseStore):
        namespace = ('agent_instructions',)
        instructions = store.get(namespace, key='agent_a')[0]
        _prompt = prompt_template.format(instructions=instructions.value['instructions'])
    return


@app.cell
def _():
    from langgraph.store.memory import InMemoryStore

    # A placeholder for a real embedding function
    def embed(texts: list[str]) -> list[list[float]]:
        # In a real application, use a proper embedding model
        return [[1.0, 2.0] for _ in texts]

    # Initialize an in-memory store. For production, use a database-backed store.
    store = InMemoryStore(index={"embed": embed, "dims": 2})

    # Define a namespace for a specific user and application context
    user_id = "my-user"
    application_context = "chitchat"
    namespace = (user_id, application_context)

    # 1. Put a memory into the store
    store.put(
        namespace,
        "a-memory",  # The key for this memory
        {
            "rules": [
                "User likes short, direct language",
                "User only speaks English & python",
            ],
            "my-key": "my-value",
        },
    )

    # 2. Get the memory by its namespace and key
    item = store.get(namespace, "a-memory")
    print("Retrieved Item:", item)

    # 3. Search for memories within the namespace, filtering by content
    # and sorting by vector similarity to the query.
    items = store.search(
        namespace,
        filter={"my-key": "my-value"},
        query="language preferences"
    )
    print("Search Results:", items)
    return


if __name__ == "__main__":
    app.run()
