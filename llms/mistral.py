from langchain_mistralai import ChatMistralAI

def get_mistral_llm():
    return ChatMistralAI(
       model="mistral-small-2506",
       temperature=0.7,
       max_retries=2,
       timeout=120,
    )

