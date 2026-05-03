def update_score(user_id, followed_diet, workout_done):
    import sqlite3
    conn = sqlite3.connect("fitai.db")
    cursor = conn.cursor()

    score = 0
    if followed_diet:
        score += 10
    if workout_done:
        score += 10

    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    current = cursor.fetchone()[0]

    new_score = current + score

    cursor.execute("UPDATE users SET score=? WHERE user_id=?", (new_score, user_id))
    conn.commit()
    conn.close()

    return new_score


def adjust_plan_based_on_score(score, plan):
    # rule-based adaptation
    if score < 50:
        plan["difficulty"] = "easy"
        plan["note"] = "Focus on consistency, not intensity."
    elif score < 100:
        plan["difficulty"] = "moderate"
    else:
        plan["difficulty"] = "hard"
        plan["note"] = "You are doing great, push harder!"

    return plan