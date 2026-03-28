from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Main code starts
# load the envrinment variables
load_dotenv()


# Specify the model to be used
# llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

response = llm.invoke("What is the meaning of life")
print(response)
