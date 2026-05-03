def calculate_calories(user):
    # Mifflin-St Jeor (basic)
    bmr = 10 * user["weight"] + 6.25 * user["height"] - 5 * user["age"] + 5
    
    if user["activity_level"] == "low":
        calories = bmr * 1.2
    elif user["activity_level"] == "moderate":
        calories = bmr * 1.55
    else:
        calories = bmr * 1.725

    if user["goal"] == "fat_loss":
        calories -= 300
    elif user["goal"] == "muscle_gain":
        calories += 300

    return int(calories)


def calculate_protein(user):
    if user["activity_level"] == "high":
        return round(1.8 * user["weight"])
    return round(1.2 * user["weight"])


def generate_plan(user):
    calories = calculate_calories(user)
    protein = calculate_protein(user)

    return {
        "calories": calories,
        "protein": protein
    }