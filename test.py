from dotenv import load_dotenv
load_dotenv()

try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnableSequence
    from langchain_groq import ChatGroq
except Exception as e:
    raise RuntimeError("Required packages not available in this environment.") from e

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt_template = PromptTemplate.from_template("Explain the following in 2-3 lines:\n\n{text}")
chain = RunnableSequence(prompt_template, llm)

def extract_text(result):
    if hasattr(result, "content"):
        return getattr(result, "content")
    if isinstance(result, dict):
        for key in ("content", "text", "output"):
            if key in result:
                return result[key]
    return str(result)

def main():
    user_input = input("Enter the text or prompt (leave empty to use default): ").strip()
    if not user_input:
        user_input = "The importance of data privacy in healthcare AI."
    try:
        result = chain.invoke({"text": user_input})
        print("Model output:\n", extract_text(result))
    except Exception as err:
        print("Error invoking the chain:", err)

if __name__ == "__main__":
    main()