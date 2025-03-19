from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from tools import get_all_meals,get_and_update_old_meals,create_meal_graph, get_all_meals,tool



# Load API keys securely
import json
with open('config.json') as f:
    config = json.load(f)
ANTHROPIC_API_KEY = config["ANTHROPIC_API_KEY"]

# Meal Checker Supervisor: Retrieves 4 meals from Neo4j
model2 = ChatAnthropic(model="claude-3-7-sonnet-20250219", api_key=ANTHROPIC_API_KEY)
model = ChatAnthropic(model="claude-3-5-haiku-20241022", api_key=ANTHROPIC_API_KEY)

meal_checker = create_react_agent(
    model=model,
    tools=[get_and_update_old_meals],
    name="meal_checker",
    prompt="""
You are a meal planner assistant that first checks the user's previous meal history using the get_and_update_old_meals function.
You must:
1️⃣ Query the database to get ** meals that have not been shown to the user in the last 2 weeks** by calling `get_and_update_old_meals(meal_plan)`.
2️⃣ Present these meals to the user and ask **if they would like to proceed with them**.
3️⃣ If the user agrees, **log that these meals have been shown today** and pass them to the next agent.
4️⃣ If the user does not agree, instruct the personal chef to generate new meals.

Return the selected meals in the following JSON format:
{
  "use_existing_meals": <true/false>,
  "selected_meals": [
    {
      "day": <number>,
      "name": <string>,
      "instructions": <string>
    },
    ...
  ]
}"""
)

personal_chef = create_react_agent(
    model=model,
    tools=[tool,get_all_meals],
    name="personal_chef",
    prompt="""You are a personal chef who specializes in crafting healthy, balanced vegetarian meal use the tool to genarte meals. 
    check if the meal is present in data base using is_meal_in_db.
    
Plan **vegetarian dinners** that are balanced and nutritious. You are an expert in creating delicious, healthy meal options 
for a young, active individual. Each meal should contain **carbohydrates, protein, and fiber**.

For each meal, provide the following details:
- **Meal Name**
- **Main Ingredients**
- **Protein Source**
- **Cooking Method**
- **Step-by-step Cooking Instructions**

Return the meals in this **structured JSON format**:
{
  "meal_plan": [
    {
      "name": <string>,
      "main_ingredients": [<string>, ...],
      "protein_source": [<string>, ...],
      "cooking_method": <string>,
      "instructions": <detailed step-by-step instructions as a string>
    },
    {
      "name": <string>,
      "main_ingredients": [<string>, ...],
      "protein_source": [<string>, ...],
      "cooking_method": <string>,
      "instructions": <detailed step-by-step instructions as a string>
    }
  ]
}
"""
)


meal_pusher = create_react_agent(
    model=model,
    tools=[get_all_meals, create_meal_graph],
    name="meal_pusher",
    prompt="""You are responsible for adding newly generated meals into the Neo4j database.
    
Follow these steps:
1️⃣ **Ensure each new meal is not already in the database using get_all_meals. Get the optimized meals if it**
2️⃣ **If a meal is new, insert it into Neo4j using create_meal_graph** with last_shown set to today's date.
3️⃣ **Link ingredients** to the meal and label proteins properly.
input : make sure the meals are structured in this way before you pass it to create_meal_graph
example1:
{
        "name": "Vegetarian Quinoa Bowl",
        "instructions": "Cook quinoa and roast vegetables.",
        "main_ingredients": ["quinoa", "broccoli", "bell peppers"],
        "protein_source": ["quinoa"]
}

Return confirmation in this JSON format:
{
  "pushed_meals": [<list of meal names successfully added>]
}"""
)


menu_optimizer = create_react_agent(
    model=model,
    tools=[],  # No external tools needed for this agent
    name="menu_optimizer",
    prompt="""Your expertise in cooking techniques and recipes allows you to suggest appropriate replacements for ingredients 
that maintain the overall nutritional balance of the menu. Your task is to determine when to swap one ingredient for another, 
ensuring that every meal's nutritional needs are met while consolidating the recipes to use the fewest unique ingredients possible. 
Optimize the menu so that ingredient variety is minimized without compromising taste, quality, or the clarity of the cooking instructions."""
)

grocery_shopper = create_react_agent(
    model=model,
    tools=[],  # No external tools needed.
    name="grocery_shopper",
    prompt="""You are a professional grocery shopper who converts a meal plan into a structured shopping list.
Given a meal plan, generate an ordered list of ingredients that consolidates items for efficient shopping.
Return the grocery list as a JSON array of strings under the key "grocery_list"."""
)





