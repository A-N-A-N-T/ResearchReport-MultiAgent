from llms.gemini import gemini_AI
from llms.mistral import get_mistral_llm
from llms.openAi import openAI_llm

_llm = None


def set_llm(choice):
    global _llm

    choice = choice.lower()

    if choice == "mistral":
        _llm = get_mistral_llm()

    elif choice == "gemini":
        _llm = gemini_AI()

    elif choice == "openai":
        _llm = openAI_llm()

    else:
        raise ValueError("Unsupported LLM")


def get_llm():
    if _llm is None:
        raise ValueError("LLM has not been initialized. Call set_llm() first.")
    return _llm