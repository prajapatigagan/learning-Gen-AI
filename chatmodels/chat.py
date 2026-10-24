from dotenv import load_dotenv

load_dotenv()

# # use groq

# from langchain.chat_models import init_chat_model

# model = init_chat_model(
# "openai/gpt-oss-120b",
# model_provider="groq",
# temperature=0.7
# )

# response=model.invoke("give me peragraph in machine learning")
# print(response.content)

# # second type

# from langchain_groq import ChatGroq

# model = ChatGroq(model="openai/gpt-oss-120b")

# response=model.invoke("give me peragraph in machine learning")
# print(response.content)

# # use mistral
# from langchain_mistralai import ChatMistralAI

# model = ChatMistralAI(
#     model="mistral-small-latest",
#     temperature=0.7
# )
# response = model.invoke(
#     "Write a paragraph about machine learning."
# )
# print(response.content)

# use open router
from langchain_openai import ChatOpenAI
import os

model = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
    max_completion_tokens=100000
)

response = model.invoke(
    "Write one clear paragraph explaining machine learning. "
    "Give only the final paragraph, without planning or commentary."
)

print(response.content)