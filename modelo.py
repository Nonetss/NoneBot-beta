from langchain.schema import HumanMessage
from langchain_ollama import OllamaLLM

from template import crear_prompt

llm = OllamaLLM(model="llama3.2")

prompt_template = crear_prompt("Como te llamas?")

respuesta = llm.invoke(prompt_template.format_prompt())

print(respuesta)
