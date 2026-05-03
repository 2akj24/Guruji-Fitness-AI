from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
import sqlite3

from database import create_table
from engine import generate_plan
from meal_engine import filter_meals
from scoring import adjust_plan_based_on_score, update_score

app = Flask(__name__)

load_dotenv()
OPENROUTER_API_KEY = os.getenv("API_KEY")

# Initialize DB
create_table()


def save_user(data):
    conn = sqlite3.connect("fitai.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (age, weight, height, goal, diet_type, activity_level, budget, region, time_pref)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("age"),
        data.get("weight"),
        data.get("height"),
        data.get("goal"),
        data.get("diet_type"),
        data.get("activity_level"),
        data.get("budget"),
        data.get("region"),
        data.get("time_pref")
    ))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return user_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_plan', methods=['POST'])
def get_plan():
    try:
        data = request.form.to_dict()

        # Convert numeric fields
        data["age"] = int(data.get("age", 20))
        data["weight"] = float(data.get("weight", 70))
        data["height"] = float(data.get("height", 170))

        # Save user
        user_id = save_user(data)

        # Generate base plan (Rule-Based ML)
        plan = generate_plan(data)

        # Get personalized meals
        meals = filter_meals(data, plan["calories"])
        plan["meals"] = meals

        # Apply scoring logic (initial score = 0)
        plan = adjust_plan_based_on_score(0, plan)

        # Convert meals to text
        meal_text = ", ".join([m["name"] for m in meals])

        # LLM prompt (ONLY formatting now)
        prompt = f"""
            Return ONLY the BODY content in HTML.
            Do NOT wrap output in ``` or markdown code blocks.
            Use only:
            <h3>, <p>, <ul>, <li>, <br>

            User Details:
            Weight: {data['weight']}
            Goal: {data['goal']}
            Calories: {plan['calories']}
            Protein: {plan['protein']}
            Diet Type: {data['diet_type']}

            Meals available:
            {meal_text}

            STRICT DIET RULES (MUST FOLLOW):
            - If Diet Type = veg → NO eggs, NO chicken, NO fish
            - If Diet Type = eggetarian → eggs allowed, NO chicken or fish
            - If Diet Type = nonveg → everything allowed

            If you break these rules, the answer is incorrect.

            ---

            Start with a warm personalized greeting based on body condition 
            (underweight / overweight / obese based on weight roughly).

            Generate a clean 1-week plan.

            Each day must include:
            - Early morning drink
            - Breakfast
            - Lunch
            - Evening snack
            - Dinner
            - Calorie and protein intake of that type in front of every diet.

            Use emojis for readability.

            At the end:
            - Give hydration + tips
            - Add workout split (bro split with exercises)
            - Add motivational quote
            - End with personalized Guruji message


            """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-001",
                "messages": [{"role": "user", "content": prompt}]
            }),
            timeout=15
        )

        if response.status_code != 200:
            return jsonify({"plan": "API Error"}), 500

        result = response.json()

        return jsonify({
            "plan": result['choices'][0]['message']['content'],
            "raw_plan": plan,
            "user_id": user_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 👉 NEW ROUTE (SCORING SYSTEM)
@app.route('/update_progress', methods=['POST'])
def update_progress():
    try:
        data = request.json

        user_id = data["user_id"]
        followed_diet = data["followed_diet"]
        workout_done = data["workout_done"]

        new_score = update_score(user_id, followed_diet, workout_done)

        return jsonify({"new_score": new_score})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)