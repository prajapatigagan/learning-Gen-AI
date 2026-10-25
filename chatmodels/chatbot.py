from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
import os

model = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.9,
    max_completion_tokens=100000
)
print("chosse your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode ")
print("press 3 for sad mode")

choice = int(input("tell your response :- "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."

messages=[
    SystemMessage(content=mode)
]

# continew run nonstop
print("------Welcome Type 0 to exit the application------")
while True:
    prompt=input("You :")
    messages.append(HumanMessage(content=prompt))
    if prompt=="0":
        break
    response=model.invoke(prompt)
    messages.append(AIMessage(content=response.content))
    print("Bot :",response.content)
print(messages)    