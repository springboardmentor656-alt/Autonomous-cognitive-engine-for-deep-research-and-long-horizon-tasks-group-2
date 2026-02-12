from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
prompt = PromptTemplate.from_template("\n\n{text}")
chain = RunnableSequence(prompt, llm)

user_input = input("Enter topic (leave empty for default): ").strip()
if not user_input:
    user_input = ""

result = chain.invoke({"text": user_input})

text = getattr(result, "content", None)
if text is None:
    try:
        text = result["content"]
    except Exception:
        text = str(result)
print(text)