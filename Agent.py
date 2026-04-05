"""
agent.py — Minimal wiring: load tools → connect to Cohere → run
"""

import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain.agents import create_agent

# ------------------ LOAD ENV ------------------
load_dotenv()

# ------------------ CHECK API KEY ------------------
if not os.getenv("COHERE_API_KEY"):
    raise ValueError("COHERE_API_KEY not found in .env file")

from langchain_core.messages import SystemMessage

from tools import ALL_TOOLS          # ← import all 14 tools

load_dotenv()

if not os.getenv("COHERE_API_KEY"):
    raise ValueError("COHERE_API_KEY not found in .env")

SYSTEM_PROMPT = """You are a helpful AI assistant.
You have access to calculator, date/time, unit converter, file I/O, and web search tools.
Reason step-by-step before using a tool. Be concise and accurate."""
llm = ChatCohere(
    model="command-xlarge-nightly",
    temperature=0
)
agent = create_agent(llm, ALL_TOOLS)


def chat(query: str) -> str:
    result = agent.invoke({
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            ("user", query),
        ]
    })
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Agent ready. Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        print("AI:", chat(q), "\n")