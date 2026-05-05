import sqlite3


def update_score(user_id, followed_diet, workout_done):
    conn = sqlite3.connect("fitai.db")
    cursor = conn.cursor()

    # Calculate points
    points = 0
    if followed_diet:
        points += 5
    if workout_done:
        points += 5

    # Insert progress log
    cursor.execute("""
        INSERT INTO progress (user_id, score, followed_diet, workout_done)
        VALUES (?, ?, ?, ?)
    """, (user_id, points, int(followed_diet), int(workout_done)))

    conn.commit()

    # Get total score for this user
    cursor.execute("""
        SELECT SUM(score) FROM progress WHERE user_id = ?
    """, (user_id,))
    total = cursor.fetchone()[0] or 0

    conn.close()
    return total


def adjust_plan_based_on_score(score, plan):
    if score >= 50:
        plan["calories"] += 100
        plan["protein"] += 5
        plan["level"] = "Advanced"
    elif score >= 20:
        plan["level"] = "Intermediate"
    else:
        plan["level"] = "Beginner"
    return plan


def get_user_history(user_id):
    conn = sqlite3.connect("fitai.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, followed_diet, workout_done, logged_at
        FROM progress
        WHERE user_id = ?
        ORDER BY logged_at DESC
        LIMIT 10
    """, (user_id,))

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows