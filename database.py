import sqlite3

def get_conn():
    return sqlite3.connect("fitai.db")

def create_table():
    conn = get_conn()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        weight REAL,
        height REAL,
        goal TEXT,
        diet_type TEXT,
        activity_level TEXT,
        budget TEXT,
        region TEXT,
        time_pref TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Meals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        calories INTEGER,
        protein INTEGER,
        region TEXT,
        budget TEXT,
        time_pref TEXT,
        diet_type TEXT,
        meal_time TEXT
    )
    """)

    # Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER DEFAULT 0,
        followed_diet INTEGER DEFAULT 0,
        workout_done INTEGER DEFAULT 0,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    # Seed meals only if table is empty
    cursor.execute("SELECT COUNT(*) FROM meals")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_meals(cursor)
        conn.commit()

    conn.close()


def seed_meals(cursor):
    meals = [
        # North Indian - Veg - Low Budget - Quick
        ("Poha", 250, 6, "north", "low", "quick", "veg", "breakfast"),
        ("Bread Upma", 220, 7, "north", "low", "quick", "veg", "breakfast"),
        ("Banana Shake", 300, 10, "north", "low", "quick", "veg", "breakfast"),
        ("Dal Tadka", 350, 18, "north", "low", "quick", "veg", "lunch"),
        ("Rajma Chawal", 450, 20, "north", "low", "medium", "veg", "lunch"),
        ("Chole Bhature", 500, 16, "north", "low", "medium", "veg", "lunch"),
        ("Paneer Bhurji", 300, 20, "north", "low", "quick", "veg", "dinner"),
        ("Aloo Paratha", 350, 8, "north", "low", "medium", "veg", "breakfast"),
        ("Moong Dal Chilla", 200, 14, "north", "low", "quick", "veg", "breakfast"),
        ("Palak Paneer", 320, 18, "north", "medium", "medium", "veg", "dinner"),

        # North Indian - Non Veg - Low Budget
        ("Egg Bhurji", 250, 18, "north", "low", "quick", "nonveg", "breakfast"),
        ("Boiled Eggs + Toast", 280, 20, "north", "low", "quick", "nonveg", "breakfast"),
        ("Chicken Curry + Rice", 520, 38, "north", "low", "medium", "nonveg", "lunch"),
        ("Egg Fried Rice", 400, 18, "north", "low", "quick", "nonveg", "lunch"),
        ("Chicken Keema", 430, 35, "north", "low", "medium", "nonveg", "dinner"),
        ("Omelette Roll", 300, 20, "north", "low", "quick", "nonveg", "breakfast"),
        ("Chicken Soup", 180, 22, "north", "low", "quick", "nonveg", "dinner"),
        ("Mutton Curry + Roti", 550, 40, "north", "medium", "long", "nonveg", "dinner"),

        # South Indian - Veg - Low Budget
        ("Idli Sambar", 250, 10, "south", "low", "quick", "veg", "breakfast"),
        ("Masala Dosa", 320, 8, "south", "low", "medium", "veg", "breakfast"),
        ("Upma", 220, 7, "south", "low", "quick", "veg", "breakfast"),
        ("Rasam Rice", 300, 8, "south", "low", "quick", "veg", "lunch"),
        ("Sambar Rice", 380, 14, "south", "low", "medium", "veg", "lunch"),
        ("Pongal", 350, 10, "south", "low", "medium", "veg", "breakfast"),
        ("Coconut Chutney Sandwich", 200, 6, "south", "low", "quick", "veg", "snack"),
        ("Vegetable Uttapam", 280, 9, "south", "low", "medium", "veg", "breakfast"),

        # South Indian - Non Veg
        ("Fish Curry + Rice", 480, 35, "south", "low", "medium", "nonveg", "lunch"),
        ("Prawn Masala + Rice", 500, 32, "south", "medium", "medium", "nonveg", "dinner"),
        ("Egg Dosa", 310, 16, "south", "low", "quick", "nonveg", "breakfast"),
        ("Chicken Chettinad", 520, 40, "south", "medium", "long", "nonveg", "dinner"),

        # All Regions - Budget Friendly Snacks / Drinks
        ("Oats Smoothie", 250, 10, "all", "low", "quick", "veg", "breakfast"),
        ("Banana + Peanut Butter", 320, 12, "all", "low", "quick", "veg", "snack"),
        ("Sprouts Salad", 180, 14, "all", "low", "quick", "veg", "snack"),
        ("Curd Rice", 280, 9, "all", "low", "quick", "veg", "lunch"),
        ("Sattu Drink", 200, 12, "all", "low", "quick", "veg", "breakfast"),
        ("Chana Chaat", 220, 10, "all", "low", "quick", "veg", "snack"),
        ("Whey + Banana Shake", 350, 28, "all", "medium", "quick", "nonveg", "breakfast"),
        ("Greek Yogurt + Nuts", 300, 18, "all", "medium", "quick", "veg", "snack"),
        ("Tofu Stir Fry", 310, 22, "all", "medium", "quick", "veg", "dinner"),
        ("Paneer Salad", 270, 20, "all", "medium", "quick", "veg", "snack"),

        # North Indian Premium Veg
        ("Paneer Butter Masala", 450, 20, "north", "high", "medium", "veg", "dinner"),
        ("Dal Makhani", 400, 18, "north", "high", "long", "veg", "lunch"),

        # Premium Non-Veg
        ("Chicken Biryani", 600, 35, "north", "high", "long", "nonveg", "lunch"),
        ("Grilled Chicken Breast", 350, 40, "all", "high", "medium", "nonveg", "dinner"),

        # South Premium
        ("Ghee Roast Dosa", 420, 10, "south", "high", "medium", "veg", "breakfast"),
        ("Fish Fry", 450, 35, "south", "high", "medium", "nonveg", "dinner"),

        # Snacks Premium
        ("Almond Smoothie", 300, 12, "all", "high", "quick", "veg", "snack"),
        ("Protein Shake (Plant)", 280, 25, "all", "high", "quick", "veg", "snack"),
    ]

    cursor.executemany("""
    INSERT INTO meals (name, calories, protein, region, budget, time_pref, diet_type, meal_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, meals)