from dotenv import load_dotenv

load_dotenv()

import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm=HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1", 
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    task="text-generation",
    max_new_tokens=256
)

model=ChatHuggingFace(llm=llm)

response=model.invoke("who are you")
print(response.content)
