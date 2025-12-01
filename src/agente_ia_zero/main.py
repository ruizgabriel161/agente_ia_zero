from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("ollama:llama3.2")

system_message = SystemMessage("""Você é um guia de estudos sobre python. Quero que me explique de forma mais simples possível.\n
Use exemplos práticos e analogias para facilitar o entendimento.
Responde em portugues e se aprofunde em Type Hints.\n
As próximas mensagens serão minhas dúvidas sobre python.
""")

human_mensage = HumanMessage(content="O que são Type Hints em Python?")
message = [system_message, human_mensage]


response = llm.invoke(message)

print(response)
