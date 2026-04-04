# 🤖 LangGraph + Cohere AI Agent

A simple AI agent built using LangGraph and Cohere that can intelligently perform arithmetic operations using tool calling.

---

## 🚀 Features

* 🔧 Tool-based architecture (LangGraph)
* ➕ Addition tool
* ➖ Subtraction tool
* 🧠 LLM-powered reasoning using Cohere
* 🔐 Secure API key management using `.env`
* 💬 Interactive CLI interface

---

## 🏗️ Tech Stack

* LangGraph
* LangChain
* Cohere (LLM)
* Python
* dotenv

---

## 📂 Project Structure

```
.
├── app.py              # Main agent code
├── requirements.txt    # Dependencies
├── .env                # API key (not pushed)
├── .gitignore          # Ignore sensitive files
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/Agent_base.git
cd Agent_base
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Add Cohere API Key

Create a `.env` file in the root directory:

```
COHERE_API_KEY=your_api_key_here
```

---

### 4. Run the Agent

```
python app.py
```

---

## 💡 Example Usage

```
You: add 10 and 5
AI: 15

You: subtract 7 from 20
AI: 13
```

---

## 🧠 How It Works

1. User enters a query
2. LangGraph agent processes the input
3. Cohere LLM decides which tool to use
4. Tool executes (add / subtract)
5. Result is returned to the user

---

## 🔒 Security

* API keys are stored securely using `.env`
* `.env` is excluded via `.gitignore`

---

## 🚀 Future Improvements

* ✖️ Multiplication & Division tools
* 🧠 Memory support (chat history)
* 📄 Instruction-based agents (.md driven)
* 🔗 MCP tool integration
* 🌐 Web UI using Flask / React

---

## 👨‍💻 Author

Divyanshi Manaduli

---

## ⭐ Contribute

Feel free to fork the repo and submit pull requests!

---
