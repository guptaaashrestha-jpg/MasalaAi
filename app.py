from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re

app = Flask(__name__)
CORS(app)

# ── Admin sets the key here (or via environment variable) ──────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
# ──────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cook", methods=["POST"])
def cook():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    spices      = data.get("spices", [])
    cuisine     = data.get("cuisine", "Indian")

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ing_list   = ", ".join(ingredients)
    spice_list = ", ".join(spices) if spices else "salt and oil"

    prompt = f"""You are MasalaAI, a friendly home chef specializing in quick cooking for Indian households.

User has these ingredients: {ing_list}
Available spices/condiments: {spice_list}
Desired cuisine: {cuisine}
STRICT constraint: total prep + cook time must be UNDER 30 minutes.

Generate a delicious, practical recipe. Respond ONLY with a valid JSON object — no markdown fences, no extra text.

JSON structure:
{{
  "name": "Recipe Name",
  "cuisine": "{cuisine}",
  "totalTime": "X mins",
  "difficulty": "Easy | Medium",
  "description": "2-3 sentence appetizing description",
  "ingredients": ["200g paneer, cubed", "2 onions, sliced", ...],
  "steps": ["Step 1 instruction", "Step 2 instruction", ...],
  "nutrition": {{
    "calories": "~350 kcal",
    "protein": "18g",
    "carbs": "32g",
    "fat": "14g",
    "fiber": "5g"
  }},
  "substitutions": [
    {{"original": "paneer", "substitute": "tofu or cottage cheese", "note": "Works perfectly for a vegan version"}},
    {{"original": "cream", "substitute": "coconut milk", "note": "Adds a nice tropical flavour"}}
  ]
}}

Use ONLY the listed ingredients + spices. Keep steps clear and beginner-friendly."""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        # strip any accidental markdown fences
        clean = re.sub(r"```json|```", "", raw).strip()
        recipe = json.loads(clean)
        return jsonify(recipe)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to parse recipe JSON: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
