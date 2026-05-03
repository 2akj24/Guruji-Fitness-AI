meals_db = [
    {"name": "paneer bhurji", "calories": 300, "protein": 20, "region": "north", "budget": "low", "time": "quick"},
    {"name": "dal chawal", "calories": 400, "protein": 15, "region": "north", "budget": "low", "time": "medium"},
    {"name": "tofu stir fry", "calories": 350, "protein": 25, "region": "south", "budget": "medium", "time": "quick"},
    {"name": "oats smoothie", "calories": 250, "protein": 10, "region": "all", "budget": "low", "time": "quick"},
]


def filter_meals(user, target_calories):
    filtered = []

    for meal in meals_db:
        if (
            (meal["region"] == user["region"] or meal["region"] == "all") and
            meal["budget"] == user["budget"] and
            meal["time"] == user["time_pref"]
        ):
            filtered.append(meal)

    # simple selection
    total = 0
    selected = []

    for meal in filtered:
        if total + meal["calories"] <= target_calories:
            selected.append(meal)
            total += meal["calories"]

    return selected