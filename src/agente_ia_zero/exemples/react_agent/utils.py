from langchain.chat_models import init_chat_model, BaseChatModel


def load_llm() -> BaseChatModel:
    """
    Função responsavel por chamar a llm
    """
    return init_chat_model(
        "ollama:llama3.2", base_url="http://127.0.0.1:11434"
    )
