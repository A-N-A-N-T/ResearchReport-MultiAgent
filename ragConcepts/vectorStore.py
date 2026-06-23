from langchain_community.vectorstores import FAISS
from ragConcepts.embeddingModel import embedding_model

def create_vectorStore(chunks):
    """
     creating a vector Store using chunks created by report_col
    """

    vector_store = FAISS.from_documents(
        documents = chunks,
        embedding=embedding_model
    )

    return vector_store