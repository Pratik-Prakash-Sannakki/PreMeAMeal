
# 🧠 Multi-Agent AI System for Knowledge Retrieval

**💡 Ever been to Trader Joe’s with a grocery list and left with everything BUT what you needed? 🤦‍♂️**
I’ve been there! Meal prepping was always a struggle for me, most of the time I don't really know what to cook and the days I do– I’d buy a ton of stuff I didn’t need, forget essential ingredients, and then end up skipping meals because I didn't end up cooking. The worst part? Ingredients can get really expensive, especially when I end up at Trader Joe’s with a cart full of random items. Sound familiar?


It creates a weekly meal prep plan, 7 dishes a week(Indian, Thai, Italian) with cooking instructions, optimizes my ingredients requirements( efficinet swaping ingredients still keeping dishes tasting the same), gives out a list of what I actually need, and keeps my meals balanced, nutritious, and cost-effective. 🥑🍗🍅✨


---

## 📽️ Demo

[Watch the system in action on LinkedIn](https://www.linkedin.com/posts/pratik-p-sannakki_ai-aiagents-knowledgegraphs-activity-7308016472235065344-6Uiy?utm_source=share&utm_medium=member_desktop&rcm=ACoAACvBdFoBPiT2d6ACNp294Lgy4GFR0i8fyrA)


---

## 🚀 Key Features


This project is a modular, multi-agent system designed for intelligent knowledge retrieval and reasoning using LLMs and vector databases. Built with LangGraph, LangChain, and Streamlit, the system orchestrates agents and supervisors to collaboratively solve complex tasks with chain-of-thought decomposition, search, and tool usage.

- **Multi-Agent Architecture**: Modular agent design (via `agents.py`) with distinct roles, like planner, retriever, and solver.
- **Supervisor Graph**: Manages agent workflows using `langgraph-supervisor` (in `supervisors.py`) to ensure traceable, goal-directed execution.
- **Tool Integration**: Integrates tools like web search (`tavily`) and Neo4j graph queries (`tools.py`) to enhance agent capabilities.
- **Streamlit Frontend**: Lightweight, interactive UI (`app.py`) for prompting the agent team and viewing results.
- **Configurable & Extensible**: Uses `config.json` for credentials and is easy to expand with more tools or agent roles.

---

## 📁 Project Structure

```bash
.
├── agents.py            # Defines individual LangChain agents (retriever, solver, planner, etc.)
├── supervisors.py       # LangGraph supervisor and graph logic for orchestrating agent workflows
├── tools.py             # Utility tools used by agents (Neo4j, Tavily, etc.)
├── app.py               # Streamlit app for running queries through the system
├── config.json          # Configuration for API keys and service credentials
├── requiremnets.txt     # Required Python packages
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requiremnets.txt
```

### 4. Configure Credentials

Edit `config.json` with your actual API keys and Neo4j credentials:

```json
{
  "neo4j": {
    "uri": "bolt://localhost:7687",
    "username": "neo4j",
    "password": "your_password"
  },
  "TAVILY_API_KEY": "your_tavily_key",
  "ANTHROPIC_API_KEY": "your_claude_key",
  "LANGSMITH_API_KEY": "your_langsmith_key"
}
```

---

## 🧪 How to Use

### Launch the App:

```bash
streamlit run app.py
```

1. Enter a question or prompt into the UI.
2. The system triggers a reasoning pipeline with agents collaborating via LangGraph.
3. Outputs are shown along with agent traces and intermediate reasoning steps.

---

## 📌 Dependencies

See `requiremnets.txt` for full list. Core libraries include:

- `langchain`, `langchain-openai`, `langchain_anthropic`
- `langgraph`, `langgraph-supervisor`
- `streamlit`
- `neo4j`, `tavily-python`, `tiktoken`

---

## 🔧 Customization Tips

- **Add new agents** in `agents.py` with specific goals (e.g., summarizer, ranker).
- **Extend the graph** in `supervisors.py` to include conditional branching or retry logic.
- **Plug in tools** via `tools.py` (e.g., database lookups, file readers, APIs).
- **Log and trace** agent decisions with `LANGSMITH_API_KEY`.

---


## 👨‍💻 Author

**Pratik Sannakki**  
_Data Scientist passionate about building modular, intelligent LLM applications._

---

## 📜 License

MIT License (or specify if different)
