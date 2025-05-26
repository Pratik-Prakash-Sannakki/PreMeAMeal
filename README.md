# 🧠 Multi-Agent AI System for Smart Meal Planning & Knowledge Retrieval

**💡 Ever gone to Trader Joe’s with a list and still forgot the essentials? 🫦**

Same here! Meal prepping was always chaotic—I didn’t know what to cook, bought the wrong things, overspent, and skipped meals. Ingredients pile up. Plans fall apart. Sound familiar?

So I built a smarter way.

> This AI-powered app generates **7 balanced dishes per week** (Indian, Thai, Italian), optimizes ingredients (smart swaps that preserve flavor), and produces a consolidated, efficient grocery list. It keeps nutrition, taste, and cost-efficiency in perfect balance. 🥑🍗🍅

Designed with **innovation and efficiency** in mind, this multi-agent system combines LLM reasoning with graph-based memory to deliver practical meal plans tailored weekly.

---

## 🎩 Demo

[Watch on LinkedIn](https://www.linkedin.com/posts/pratik-p-sannakki_ai-aiagents-knowledgegraphs-activity-7308016472235065344-6Uiy?utm_source=share&utm_medium=member_desktop)

---

## 🚀 Key Features

* **Smart Meal Planning**: 2 brand new meals sourced online + 5 meals recycled from the knowledge graph (ensuring nothing is repeated within 2 weeks).
* **Ingredient Optimization**: Consolidates ingredients across meals and intelligently swaps based on availability & cost.
* **Balanced Nutrition**: Focuses on healthy, diverse, and cuisine-specific meals.
* **Persistent Knowledge**: Meals and ingredients are stored in a Neo4j graph for traceable recommendations.

---

## 🤖 Multi-Agent Architecture

### 1. 📏 Top-Level Supervisor

Coordinates the entire system.

* **Role**: Oversees meal retrieval, generation, optimization, and storage.
* **Supervises**: All subsystem supervisors.

### 2. 🚧 Workflow Supervisors

Each manages one core pipeline component:

* **Meal Checker Supervisor**

  * Retrieves meals not used in the last 2 weeks.

* **Meal Generator Supervisor**

  * Uses search + LLM to create vegetarian dishes.

* **Meal Optimization Supervisor**

  * Swaps, deduplicates, and balances ingredients.

* **Meal Pusher Supervisor**

  * Stores final plans in Neo4j graph DB.

### 3. 🧹 Specialized Agents

Agents handle core tasks with tool support:

* **Meal Checker Agent**: Uses `get_and_update_old_meals`
* **Personal Chef Agent**: Uses `TavilySearchResults` for external meal ideas
* **Meal Optimizer Agent**: Uses `optimize_ingredients_tool`
* **Meal Pusher Agent**: Uses `create_meal_graph` and `update_db`

### 4. ⚖️ Tools & Utilities

Plug-and-play tools power the agents:

* `get_and_update_old_meals`: Filters past meals
* `TavilySearchResults`: Searches new meal ideas
* `optimize_ingredients_tool`: Smart ingredient minimizer
* `create_meal_graph` & `update_db`: Structure and persist meals in Neo4j

---

## 📂 Project Structure

```bash
.
├── agents.py            # Agent roles and behaviors
├── supervisors.py       # LangGraph supervisors for agent workflows
├── tools.py             # Tools for data access, search, optimization
├── app.py               # Streamlit UI
├── config.json          # API keys & DB credentials
├── requirements.txt     # Python package dependencies
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `config.json`

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

## 🔮 How to Use

```bash
streamlit run app.py
```

1. Input your question or click "Generate Weekly Plan"
2. Agents collaborate using LangGraph to plan, optimize, and store
3. Review meal suggestions, ingredient list, and trace decisions

---

## 📊 Core Dependencies

* `langchain`, `langchain-anthropic`, `langgraph`
* `streamlit`, `neo4j`, `tavily-python`
* `tiktoken`, `pydantic`, `dotenv`

---

## 🔧 Customization

* Add new agent types in `agents.py` (e.g. NutritionistAgent)
* Expand LangGraph logic in `supervisors.py`
* Add new tools in `tools.py`
* Log and trace performance using LangSmith

---

## 👨‍💼 Author

**Pratik Sannakki**
*Data Scientist passionate about building intelligent, modular AI systems.*

---

## 📚 License

MIT License
