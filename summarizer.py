from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 🔹 Toggle this if you want to disable real LLM
USE_REAL_LLM = True

chain = None

if USE_REAL_LLM:
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",  # ✅ supported Groq model
            temperature=0
        )

        prompt = ChatPromptTemplate.from_template(
            "Summarize the following text clearly and concisely:\n\n{text}"
        )

        chain = prompt | llm | StrOutputParser()

    except Exception as e:
        print("⚠️ LLM init failed, using fallback summary.")
        print(e)
        chain = None


def summarize(text: str) -> str:
    # ✅ Real LLM path
    if USE_REAL_LLM and chain is not None:
        return chain.invoke({"text": text})

    # ✅ Fallback path (NO LLM, NO CRASH)
    if not text:
        return ""

    snippet = text.strip()
    if len(snippet) <= 200:
        return "[Summary] " + snippet

    return "[Summary] " + snippet[:197].rstrip() + "..."
