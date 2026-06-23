def get_retriever(vector_store):
    """
     Convert FAISS vector store into a retriver.
    """

    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs={
            "k": 4
        }
    )

    return retriever