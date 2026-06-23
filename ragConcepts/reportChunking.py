from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_report(report : str):
    """
     Split the generated research report into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 80,
        separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )
    chunks = splitter.create_documents([report])

    return chunks



