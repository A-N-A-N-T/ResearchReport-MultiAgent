from langchain_core.output_parsers import StrOutputParser
from agents import llm
from ragConcepts.ragPrompt import prompt

parser = StrOutputParser()

rag_chain = prompt | llm | parser

def QuestionAnswer(Question,retriever):
    """
     Ask questions about the generated research report.
    """

    docs = retriever.invoke(Question)

    context = "\n\n".join(
        doc.page_content for doc in docs 
    )

    answer = rag_chain.invoke(
        {
            "context": context,
            "question" : Question
        }
    )
    return answer
