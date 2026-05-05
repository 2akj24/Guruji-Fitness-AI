from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
import sqlite3

from database import create_table
from engine import generate_plan
from meal_engine import filter_meals
from scoring import adjust_plan_based_on_score, update_score, get_user_history

app = Flask(__name__)

load_dotenv()
OPENROUTER_API_KEY = os.getenv("API_KEY")

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


def generate_workout_plan(activity_level):
    if activity_level == "low":
        return """
Activity Level: Low
Workout Style: Beginner-friendly 3 days/week

Day 1: Full Body
- Bodyweight Squats: 3 sets x 12 reps
- Push-ups: 3 sets x 8 reps
- Plank: 3 sets x 30 seconds

Day 2: Rest + 20 minute walk

Day 3: Upper Body
- Incline Push-ups: 3 sets x 10 reps
- Dumbbell Shoulder Press: 3 sets x 12 reps
- Dumbbell Rows: 3 sets x 12 reps

Day 4: Rest

Day 5: Lower Body
- Squats: 3 sets x 12 reps
- Lunges: 3 sets x 10 reps
- Calf Raises: 3 sets x 15 reps

Day 6: Light walk + stretching
Day 7: Rest
"""

    elif activity_level == "moderate":
        return """
Activity Level: Moderate
Workout Style: 4 days/week Upper-Lower Split

Day 1: Upper Body
- Bench Press / Push-ups: 4 sets x 10 reps
- Rows: 4 sets x 10 reps
- Shoulder Press: 3 sets x 12 reps
- Biceps Curls: 3 sets x 12 reps

Day 2: Lower Body
- Squats: 4 sets x 10 reps
- Lunges: 3 sets x 12 reps
- Leg Curl: 3 sets x 12 reps
- Calf Raises: 4 sets x 15 reps

Day 3: Rest / Walk

Day 4: Upper Body
- Incline Press: 4 sets x 10 reps
- Lat Pulldown: 4 sets x 10 reps
- Lateral Raises: 3 sets x 15 reps
- Triceps Pushdown: 3 sets x 12 reps

Day 5: Lower Body
- Deadlift: 3 sets x 8 reps
- Leg Press: 4 sets x 10 reps
- Hamstring Curl: 3 sets x 12 reps
- Abs: 3 sets

Day 6: Cardio + Mobility
Day 7: Rest
"""

    else:
        return """
Activity Level: High
Workout Style: 6 days/week Push Pull Legs

Day 1: Push
- Bench Press: 4 sets x 8-10 reps
- Shoulder Press: 4 sets x 10 reps
- Incline Dumbbell Press: 3 sets x 12 reps
- Triceps Pushdown: 3 sets x 12 reps

Day 2: Pull
- Pull-ups / Lat Pulldown: 4 sets x 10 reps
- Barbell Rows: 4 sets x 10 reps
- Face Pulls: 3 sets x 15 reps
- Biceps Curls: 3 sets x 12 reps

Day 3: Legs
- Squats: 4 sets x 8-10 reps
- Romanian Deadlift: 4 sets x 10 reps
- Leg Press: 3 sets x 12 reps
- Calf Raises: 4 sets x 15 reps

Day 4: Push
Day 5: Pull
Day 6: Legs
Day 7: Rest
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_plan', methods=['POST'])
def get_plan():
    try:
        data = request.form.to_dict()

        data["age"] = int(data.get("age", 20))
        data["weight"] = float(data.get("weight", 70))
        data["height"] = float(data.get("height", 170))

        existing_user_id = data.get("user_id")

        if existing_user_id and existing_user_id.isdigit():
            user_id = int(existing_user_id)
        else:
            user_id = save_user(data)

        plan = generate_plan(data)

        meals = filter_meals(data, plan["calories"])
        plan["meals"] = meals

        plan = adjust_plan_based_on_score(0, plan)

        workout_text = generate_workout_plan(data.get("activity_level", "low"))

        meal_text = "\n".join([
            f"- {m['meal_time']}: {m['name']} | {m['calories']} kcal | "
            f"{m['protein']}g protein | Region: {m['region']} | "
            f"Budget: {m['budget']} | Time: {m['time_pref']} | Diet: {m['diet_type']}"
            for m in meals
        ])

        prompt = f"""
        Return ONLY the BODY content in HTML.
        Do NOT wrap output in ``` or markdown code blocks.
        Use only these tags:
        <h3>, <p>, <ul>, <li>, <br>

        USER INPUTS:
        Age: {data['age']}
        Weight: {data['weight']} kg
        Height: {data['height']} cm
        Goal: {data['goal']}
        Diet Type: {data['diet_type']}
        Activity Level: {data['activity_level']}
        Budget: {data['budget']}
        Region Preference: {data['region']}
        Cooking Time Preference: {data['time_pref']}

        CALCULATED PLAN:
        Daily Calories: {plan['calories']}
        Daily Protein: {plan['protein']}g
        Fitness Level: {plan['level']}

        DATABASE MEALS SELECTED:
        {meal_text}

        STRICT DIET RULES:
        1. Use ONLY the meals listed in DATABASE MEALS SELECTED.
        2. Do NOT invent extra meals.
        3. Every meal must match the user's diet type.
        4. If diet_type is veg, do NOT include egg, chicken, fish, mutton, or meat.
        5. Respect budget: {data['budget']}.
        6. Respect region preference: {data['region']}.
        7. Respect cooking time preference: {data['time_pref']}.
        8. Mention calories and protein with every meal.
        9. If a meal type is missing, reuse suitable listed meals only.

        WORKOUT PLAN TO USE:
        {workout_text}

        OUTPUT FORMAT:

        Start with a warm personalized greeting based on body condition.

        <h3>Personalized 1 Week Diet Plan</h3>

        For each day include:
        <ul>
        <li>Early Morning Drink</li>
        <li>Breakfast</li>
        <li>Lunch</li>
        <li>Evening Snack</li>
        <li>Dinner</li>
        </ul>

        Each meal must show:
        Meal name, calories, and protein.

        <h3>Workout Plan Based on Activity Level</h3>

        Use the exact workout plan provided above and format it clearly.

        <h3>Hydration, Recovery & Guruji Tips</h3>
        <ul>
        <li>Hydration tip</li>
        <li>Recovery tip</li>
        <li>Motivational quote</li>
        <li>Personalized Guruji message</li>
        </ul>
        """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-001",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }),
            timeout=30
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


@app.route('/meals')
def meals():
    conn = sqlite3.connect("fitai.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meals ORDER BY region, diet_type, calories")

    all_meals = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return render_template('meals.html', meals=all_meals)


@app.route('/history/<int:user_id>')
def history(user_id):
    logs = get_user_history(user_id)

    return render_template('history.html', logs=logs, user_id=user_id)


@app.route('/api/meals')
def api_meals():
    region = request.args.get("region", "all")
    diet = request.args.get("diet_type", "veg")

    conn = sqlite3.connect("fitai.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM meals
        WHERE (region = ? OR region = 'all')
        AND diet_type = ?
        ORDER BY protein DESC
    """, (region, diet))

    results = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "count": len(results),
        "meals": results
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)