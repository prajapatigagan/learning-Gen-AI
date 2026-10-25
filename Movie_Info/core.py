from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
import os

from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
    max_completion_tokens=100000
)

prompt=ChatPromptTemplate.from_messages([
    ("system",
"""
You are Professional Movie INformation Extraction Assistant.
your task:
Extract useful structured Movie Information from a movie Peagraph and present it in a clear Instruction.
Rules:
-Do Not add explanations
-Do Not add extra commentary
-Follow the exact fromat
-If information is missing->write Null 
-Keep summary short(2-3 lines max)
- Do NOT guess unknown facts

Output format:

Movie Title:
release year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""     
     ),
     ('human',"""
Extract information from this paragraph:
{paragraph}
""")
])

para =input("Gives your paragraph :" )
final_prompt=prompt.invoke(
    {"paragraph":para}
)
response = model.invoke(final_prompt)
print(response.content)