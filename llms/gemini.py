from langchain_google_genai import ChatGoogleGenerativeAI

def gemini_AI():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )
