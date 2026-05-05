import sqlite3


def filter_meals(user, target_calories):
    conn = sqlite3.connect("fitai.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    region = user.get("region", "all")
    budget = user.get("budget", "low")
    time_pref = user.get("time_pref", "quick")
    diet_type = user.get("diet_type", "veg")

    # 1. Exact match: region + budget + time + diet
    cursor.execute("""
        SELECT * FROM meals
        WHERE (region = ? OR region = 'all')
        AND budget = ?
        AND time_pref = ?
        AND diet_type = ?
        ORDER BY meal_time, protein DESC
    """, (region, budget, time_pref, diet_type))

    rows = cursor.fetchall()

    # 2. Relax time preference
    if not rows:
        cursor.execute("""
            SELECT * FROM meals
            WHERE (region = ? OR region = 'all')
            AND budget = ?
            AND diet_type = ?
            ORDER BY meal_time, protein DESC
        """, (region, budget, diet_type))
        rows = cursor.fetchall()

    # 3. Relax budget
    if not rows:
        cursor.execute("""
            SELECT * FROM meals
            WHERE (region = ? OR region = 'all')
            AND diet_type = ?
            ORDER BY meal_time, protein DESC
        """, (region, diet_type))
        rows = cursor.fetchall()

    # 4. Final fallback
    if not rows:
        cursor.execute("""
            SELECT * FROM meals
            WHERE diet_type = ?
            ORDER BY protein DESC
            LIMIT 8
        """, (diet_type,))
        rows = cursor.fetchall()

    conn.close()

    selected = []
    total_calories = 0

    for row in rows:
        meal = dict(row)

        if total_calories + meal["calories"] <= target_calories:
            selected.append(meal)
            total_calories += meal["calories"]

    return selected