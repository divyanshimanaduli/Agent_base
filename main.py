import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_cohere import ChatCohere
from langchain.agents import create_agent

# ------------------ LOAD ENV ------------------
load_dotenv()

# ------------------ CHECK API KEY ------------------
if not os.getenv("COHERE_API_KEY"):
    raise ValueError("COHERE_API_KEY not found in .env file")

# ------------------ TOOLS ------------------
@tool
def add(a: int, b: int) -> int:
    """Add two numbers a and b"""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b

tools = [add, subtract]

# ------------------ LLM ------------------
llm = ChatCohere(
    model="command-xlarge-nightly",
    temperature=0
)

# ------------------ AGENT ------------------
agent = create_agent(
    model=llm,
    tools=tools
)

# ------------------ RUN ------------------
def run_agent():
    print("LangGraph + Cohere Agent (.env mode)\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            break

        try:
            response = agent.invoke({
                "messages": [("user", query)]
            })

            print("AI:", response["messages"][-1].content)

        except Exception as e:
            print("Error:", str(e))


if __name__ == "__main__":
    run_agent()