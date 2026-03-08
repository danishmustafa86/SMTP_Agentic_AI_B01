from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words"
)

prompt = template.format(topic="Machine Learning")

response = llm.invoke(prompt)

print(response.content)