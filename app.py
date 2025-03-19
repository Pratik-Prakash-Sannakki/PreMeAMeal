import streamlit as st
import time
import re
from neo4j import GraphDatabase
from supervisors import top_level_supervisor
import os

# Neo4j Connection Class
class MealQuery:
    def __init__(self, uri, password):
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    def close(self):
        self.driver.close()

    def get_meals_with_ingredients_and_protein_tags(self):
        """Fetch meals and their ingredients with protein tags from Neo4j, excluding those shown in the last week"""
        query = """
        MATCH (m:Meal)
        WHERE m.last_shown IS NULL OR date(m.last_shown) < date() - duration({weeks: 1})
        OPTIONAL MATCH (m)-[:CONTAINS]->(ing:Ingredient)
        RETURN m.name AS meal,
               m.description AS instructions,
               COLLECT(ing.name + ' (' + CASE WHEN ing:Protein THEN 'Protein' ELSE 'Non-Protein' END + ')') AS ingredients
        LIMIT 7
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]  # Convert Neo4j records to dict

# Initialize Neo4j connection
neo4j_conn = MealQuery("bolt://localhost:7687", "Pratikps1$")

def fetch_meals():
    """Retrieve meal data from the database"""
    meals_data = neo4j_conn.get_meals_with_ingredients_and_protein_tags()
    if not meals_data:
        return ["No meals found. Please generate a new meal plan."], []

    meal_texts = []
    all_ingredients = []

    for meal in meals_data:
        meal_name = f"🍲 **{meal['meal']}**"

        # Extract instructions
        instructions = meal['instructions']
        if isinstance(instructions, str):
            instruction_steps = re.split(r'\d+\.', instructions)
            instruction_steps = [step.strip() for step in instruction_steps if step.strip()]
        else:
            instruction_steps = ["No detailed instructions available."]

        meal_info = "### 📜 Instructions:\n"
        for step in instruction_steps:
            meal_info += f"- {step}\n"

        ingredients_info = "### 🛒 Ingredients:\n"
        for ingredient in meal['ingredients']:
            ingredients_info += f"- {ingredient}\n"
            all_ingredients.append(ingredient.split(" (")[0])

        meal_texts.append((meal_name, meal_info, ingredients_info))

    return meal_texts, all_ingredients

def generate_new_meal():
    """Generate a new meal plan and refresh the page"""
    # **Set flag for UI Lock & Display Loading Message**
    st.session_state["loading"] = True
    st.rerun()  # **Trigger Immediate Page Refresh**

def create_txt_file(ingredients):
    """Create a TXT file for the grocery list with UTF-8 encoding"""
    txt_path = "grocery_list.txt"
    with open(txt_path, "w", encoding="utf-8") as f:  # Force UTF-8 encoding
        f.write("Grocery List:\n\n")  # Removed emoji to prevent encoding issues
        for item in ingredients:
            f.write(f"- {item}\n")
    return txt_path

def download_grocery_list_as_txt(ingredients):
    """Generate and provide download button for the grocery list as a text file"""
    if ingredients:
        txt_path = create_txt_file(ingredients)
        with open(txt_path, "rb") as f:
            st.download_button(
                label="📥 Download Grocery List as TXT",
                data=f,
                file_name="grocery_list.txt",
                mime="text/plain"
            )
        os.remove(txt_path)  # Cleanup after download
    else:
        st.error("Please generate a meal plan first.")

def main():
    # **Check if meals should be generated**
    if "loading" in st.session_state and st.session_state["loading"]:
        st.markdown(
            """
            <style>
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(128, 128, 128, 0.5);
                z-index: 9999;
                text-align: center;
                color: white;
                font-size: 24px;
                padding-top: 20%;
            }
            </style>
            <div class='overlay'>🔄 Cooking up a fresh meal plan... Please wait!</div>
            """, 
            unsafe_allow_html=True
        )

        # **Simulating processing time**
        time.sleep(2)  
        top_level_supervisor.invoke({
            "messages": [{"role": "user", "content": "Plan a balanced vegetarian meal for the week."}]
        })
        time.sleep(2)  

        # **Update Meals in Session State**
        st.session_state["meals"], st.session_state["ingredients"] = fetch_meals()
        st.session_state["loading"] = False  # **Reset loading state**
        st.rerun()  # **Force full page refresh**

    # Personalized Greeting
    st.markdown("# 🍽️ Welcome to Your Personalized Meal Planner, Pratik! 🚀")
    st.markdown("### Your AI Chef is ready! Let's cook up something delicious! 😋")

    # Initialize session state for meals
    if "meals" not in st.session_state or "ingredients" not in st.session_state:
        st.session_state["meals"], st.session_state["ingredients"] = fetch_meals()

    meals, ingredients = st.session_state["meals"], st.session_state["ingredients"]

    if meals[0] == "No meals found. Please generate a new meal plan.":
        st.warning(meals[0])
    else:
        st.markdown("## 🍽️ **Meal Plans**")
        for meal_name, meal_info, ingredients_info in meals:
            with st.expander(meal_name, expanded=False):
                st.markdown(meal_info)
                st.markdown(ingredients_info)

        # Grocery List
        st.markdown("## 🛒 **Grocery List**")
        with st.expander("📌 View Grocery List"):
            st.markdown("### ✅ **Your Ingredients:**")
            st.markdown("\n".join([f"- {item}" for item in ingredients]))  # Proper Bullet Points
        
        # Download Button for Grocery List
        download_grocery_list_as_txt(ingredients)  

    # Meal Regeneration Section
    st.markdown("---")  # Adds a divider
    st.markdown("### 🤔 In the Mood for Something Else?")
    st.markdown("Click below and let me generate new sets of meals for you! 🍽️")
    
    if st.button("🔄 Generate New Meal Plan"):
        generate_new_meal()

if __name__ == "__main__":
    main()
