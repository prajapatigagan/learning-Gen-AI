from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import OpenAIEmbeddings
embeddings=OpenAIEmbeddings(
    model='openai/text-embedding-3-large',
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    check_embedding_ctx_length=False,
    dimensions=64
)
texts=[
    "Hello this is Gagandeep",
    "Hello your name is Megha",
    "And you all are very beautiful"
]

vector = embeddings.embed_documents(texts)
print(vector)