from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load the recipes from the updated recipes.json
def load_recipes():
    with open("recipes.json", "r") as file:
        return json.load(file)

# Function to search recipes based on at least 2 ingredients matching
def search_recipes_by_ingredients(ingredients):
    recipes = load_recipes()
    matching_recipes = []
    
    # Check if at least 2 ingredients match any recipe
    for recipe in recipes:
        match_count = 0
        for ingredient in ingredients:
            if ingredient in recipe["ingredients"]:
                match_count += 1
        # If two or more ingredients match, add the recipe to the results
        if match_count >= 2:
            matching_recipes.append(recipe)
    
    return matching_recipes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ingredients = []
        
        # Collect all the ingredients from the form
        for i in range(1, 6):  # Allow up to 5 ingredients
            ingredient = request.form.get(f"ingredient{i}")
            if ingredient:
                ingredients.append(ingredient)
        
        # After ingredients are collected, redirect to result page
        if len(ingredients) >= 2:
            return redirect(url_for('result', ingredients=','.join(ingredients)))
    
    return render_template("index.html")

@app.route("/result")
def result():
    ingredients = request.args.get("ingredients").split(',')
    
    # Get the matching recipes
    matching_recipes = search_recipes_by_ingredients(ingredients)
    
    return render_template("result.html", recipes=matching_recipes, ingredients=ingredients)

if __name__ == "__main__":
    app.run(debug=True)
