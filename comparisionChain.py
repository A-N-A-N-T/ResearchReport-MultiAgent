from langchain_core.output_parsers import StrOutputParser
from comparisionPrompt import comparePrompt
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

def compareChain():
    llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.7,
    max_retries=2,
    timeout=120,
    )
     
    return comparePrompt | llm | StrOutputParser()

