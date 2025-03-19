from langgraph_supervisor import create_supervisor
from langchain_anthropic import ChatAnthropic
from agents import meal_checker,personal_chef,menu_optimizer,grocery_shopper,meal_pusher

# Load API keys securely
import json
with open('config.json') as f:
    config = json.load(f)
ANTHROPIC_API_KEY = config["ANTHROPIC_API_KEY"]


# Meal Checker Supervisor: Retrieves 4 meals from Neo4j
model2 = ChatAnthropic(model="claude-3-7-sonnet-20250219", api_key=ANTHROPIC_API_KEY)
model = ChatAnthropic(model="claude-3-5-haiku-20241022", api_key=ANTHROPIC_API_KEY)



meal_checker_supervisor = create_supervisor(
    [meal_checker],
    model=model,
    prompt=(
        "You are responsible for retrieving ** meals from the database**."
        "These meals should not have been shown in the past 2 weeks, ensuring variety while maintaining efficiency."
        "Do not generate new meals. Fetch all ** meals** and return them."
        "Format the response as:\n"
        "{\n"
        '  "selected_meals": [\n'
        '    {\n'
        '      "name": <string>,\n'
        '      "instructions": <string>\n'
        '    },\n'
        '    ...\n'
        '  ]\n'
        "}"
    )
).compile(name="meal_checker_supervisor")


meal_generator_supervisor = create_supervisor(
    [personal_chef],
    model=model,
    prompt=(
        "<instructions>"
        "You are responsible for generating **new meals** and adding them to the database."
        "1️. **First, generate  new vegetarian meals** via `personal_chef`.\n"
        "Return confirmation of stored meals in the JSON format:\n"
        "</instructions>"
        "<Response Format>"
        "{\n"
        '  "generated_meals": [\n'
        '    {\n'
        '      "name": <string>,\n'
        '      "main_ingredients": [<string>, ...],\n'
        '      "protein_source": [<string>, ...],\n'
        '      "cooking_method": <string>,\n'
        '      "instructions": <detailed step-by-step instructions as a string>\n'
        '    }\n'
        '  ],\n'
        "}"
        "</Response Format>"
    )
).compile(name="meal_generator_supervisor")



# Meal Optimization and Grocery Supervisor: Optimizes and prepares grocery list
meal_optimization_supervisor = create_supervisor(
    [menu_optimizer, grocery_shopper],
    model=model,
    prompt=(
        "You are responsible for optimizing the meal plan and generating a structured grocery list. "
        "Ensure the ingredients are consolidated to **minimize unique ingredient purchases** while keeping meals balanced. "
        "Return the optimized meal plan and grocery list in the following JSON format:\n"
        "<Response>"
        "{\n"
        '  "optimized_meal_plan": [\n'
        '    {\n'
        '      "name": <string>,\n'
        '      "main_ingredients": [<string>, ...],\n'
        '      "protein_source": [<string>, ...],\n'
        '      "cooking_method": <string>,\n'
        '      "instructions": <detailed step-by-step instructions as a string>\n'
        '    },\n'
        '    ...\n'
        '  ],\n'
        '  "grocery_list": [<string>, ...]\n'
        "}\n"
        "</Response>"
    )
).compile(name="meal_optimization_supervisor")


# Define the meal_pusher_supervisor
meal_pusher_supervisor = create_supervisor(
    [meal_pusher],
    model=model,
    prompt=(
        "You are responsible for pushing meals into the Neo4j database. "
        "Ensure each meal is not already in the database before inserting it. "
        "make sure detailed cooking instructions are pushed to the database"
        "Return confirmation of pushed meals in the following JSON format:\n"
        "{\n"
        '  "pushed_meals": []\n'
        "}\n"
    )
).compile(name="meal_pusher_supervisor")





top_level_supervisor = create_supervisor(
    [meal_checker_supervisor, meal_generator_supervisor, meal_optimization_supervisor, meal_pusher_supervisor],
    model=model2,
    prompt=(
        "<Instructions>"
        "You manage the meal planning workflow. **Follow this sequence:**\n"
        "1. **Retrieve 4 meals** from the database via the **meal checker supervisor**.\n"
        "2. If **4 meals are not retrieved** from the **meal checker supervisor**, generate **6 new meals** via the **meal generator supervisor**; if **4 meals are retrieved**, generate only **2 new meals**.\n"
        "3. **Optimize ingredients and generate a grocery list** via the **meal optimization supervisor**.\n"
        "4. make sure the the **meal_pusher_supervisor** get all the exact same meal deatils that the **meal_optimization_supervisor** genearted \n"
        "5. Use the **meal_pusher_supervisor** to push all the optimized meals obtained from the **meal optimization supervisor** to the database.\n"
        "6. **Final Output Requirement:** The final JSON response ** MUST be the exact SAME EXACT MEALS and GROCERY LIST that were pushed to the database** do not generate any new meals names or grocery items. Ensure that all grocery items are categorized correctly under their respective sections and that the response is not truncated.\n"
        "</Instructions>"
        
        "<Response>"
        "Your response **MUST** be a valid JSON object with the following format, reflecting the meals and grocery list exactly as they were pushed to the database:\n\n"
        "```json\n"
        "{\n"
        '    "meals": ["optimized_meal 1", "optimized_meal 2", "optimized_meal 3", "optimized_meal 4", "optimized_meal 5", "optimized_meal 6"],\n'
        '    "grocery_list": {\n'
        '        "Fruits & Vegetables": ["Item1", "Item2"],\n'
        '        "Dairy": ["Item3", "Item4"],\n'
        '        "Meat & Seafood": ["Item5"],\n'
        '        "Pantry": ["Item6", "Item7"]\n'
        "    }\n"
        "}\n"
        "```\n"
        "</Response>"
    )
).compile(name="top_level_supervisor")


result = top_level_supervisor.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Plan a balanced vegetarian meal for the week."
        }
    ]
})