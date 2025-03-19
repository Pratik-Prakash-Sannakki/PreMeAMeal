from langchain_community.tools.tavily_search import TavilySearchResults
import getpass
import os
from neo4j import GraphDatabase
from datetime import date, timedelta
import json


# Load credentials from config.json
def load_credentials():
    with open('config.json') as f:
        config = json.load(f)
    return config

config = load_credentials()

# Neo4j connection details
uri = config["neo4j"]["uri"]
username = config["neo4j"]["username"]
password = config["neo4j"]["password"]

# Tavily API key
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = config["TAVILY_API_KEY"]

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

# Initialize the search tool with the API key
tool = TavilySearchResults( max_results=2)




def get_and_update_old_meals(uri, username, password):
    """Retrieve meals that have not been shown in the last 2 weeks, update their last_shown date, and return as a formatted string."""
    from neo4j import GraphDatabase
    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        # Retrieve old meals
        result = session.run(
            """
           MATCH (m:Meal)
           WHERE m.last_shown IS NULL OR m.last_shown < date() - duration({weeks: 2})
           RETURN m.name AS meal_name, m.description AS instructions
           ORDER BY m.last_shown ASC 
           limit 4
            """
        )
        
        # Process the result
        meals = [{"name": record["meal_name"], "instructions": record["instructions"]} for record in result]

        if not meals:
            driver.close()
            return "No old meals found."

        # Update last_shown date for retrieved meals
        for meal in meals:
            session.run(
                """
                MATCH (m:Meal {name: $meal_name})
                SET m.last_shown = date()
                """,
                meal_name=meal["name"]
            )

    # Close the connection
    driver.close()

    # Format and return meals as a string
    meal_list_string = "\n".join(f"- {meal['name']}: {meal['instructions']}" for meal in meals)
    return meal_list_string



def create_meal_graph(meal_plan):
    """Inserts meals into the Neo4j graph, linking them to ingredients and setting last_shown date to 3 weeks ago."""
    
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    try:
        with driver.session() as session:
            for meal in meal_plan:
                meal_name = meal["name"]
                meal_instructions = meal["instructions"]
                main_ingredients = meal["main_ingredients"]
                protein_sources = meal["protein_source"]
                three_weeks_ago = (date.today() - timedelta(weeks=3)).isoformat()
                
                # Create or update the meal node
                session.write_transaction(
                    lambda tx: tx.run(
                        """
                        MERGE (m:Meal {name: $meal_name})
                        SET m.description = $meal_instructions,
                            m.last_shown = date($three_weeks_ago)
                        """,
                        meal_name=meal_name,
                        meal_instructions=meal_instructions,
                        three_weeks_ago=three_weeks_ago
                    )
                )
                
                # Consolidate ingredients to avoid duplicates
                for ingredient in set(main_ingredients + protein_sources):
                    # Create ingredient node if it doesn't exist
                    session.write_transaction(
                        lambda tx: tx.run(
                            "MERGE (i:Ingredient {name: $ingredient})",
                            ingredient=ingredient
                        )
                    )
                    
                    # Create relationship between Meal and Ingredient
                    session.write_transaction(
                        lambda tx: tx.run(
                            """
                            MATCH (m:Meal {name: $meal_name})
                            MATCH (i:Ingredient {name: $ingredient})
                            MERGE (m)-[:CONTAINS]->(i)
                            """,
                            meal_name=meal_name,
                            ingredient=ingredient
                        )
                    )
                    
                    # Label the ingredient as Protein if applicable
                    if ingredient in protein_sources:
                        session.write_transaction(
                            lambda tx: tx.run(
                                """
                                MATCH (i:Ingredient {name: $ingredient})
                                SET i:Protein
                                """,
                                ingredient=ingredient
                            )
                        )
        print("Meals successfully pushed to the database.")
    except Exception as e:
        print("Error pushing meals to DB:", e)
    finally:
        driver.close()


def get_all_meals():
    """Retrieve all meals from the Neo4j database."""
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            result = session.run("MATCH (m:Meal) RETURN m.name AS meal_name")
            meals = [record["meal_name"] for record in result]
        driver.close()
        return meals
    except Exception as e:
        print(f"An error occurred: {e}")
        return None