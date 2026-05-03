# 🏋️ Guruji Fitness AI

> Your personal AI-powered fitness and nutrition coach — built with Python & Flask.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 About

**Guruji Fitness AI** is an intelligent fitness web application that provides personalized workout plans, meal recommendations, and fitness scoring — all powered by an AI engine built in Python. Whether you're a beginner or an athlete, Guruji adapts to your goals and guides you like a personal trainer.

---

## ✨ Features

- 🤖 **AI Fitness Engine** — Smart recommendations based on user profile and goals
- 🍽️ **Meal Planning Engine** — Personalized diet and nutrition suggestions
- 📊 **Fitness Scoring** — Track and score your fitness progress over time
- 🗃️ **User Database** — Persistent storage of user data using SQLite
- 🌐 **Web Interface** — Clean, responsive UI with Flask templates

---

## 🗂️ Project Structure

```
Guruji-Fitness-AI/
│
├── app.py              # Main Flask application & routes
├── engine.py           # Core AI fitness recommendation engine
├── meal_engine.py      # Meal planning and nutrition engine
├── scoring.py          # Fitness scoring logic
├── database.py         # Database models and helpers
├── fitai.db            # SQLite database
├── requirements.txt    # Python dependencies
│
├── static/             # CSS, JS, images
└── templates/          # HTML Jinja2 templates
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/2akj24/Guruji-Fitness-AI.git
cd Guruji-Fitness-AI

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser and go to: **http://localhost:5000**

---

## ⚙️ Configuration

Create a `.env` file in the root directory for any environment-specific settings:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

---

## 🧠 How It Works

1. **User onboards** by entering their fitness profile (age, weight, goals, etc.)
2. **`engine.py`** processes the profile and generates a personalized workout plan
3. **`meal_engine.py`** recommends meals based on the user's caloric and nutritional needs
4. **`scoring.py`** evaluates fitness progress and assigns a score
5. All data is stored and retrieved via **`database.py`** using SQLite (`fitai.db`)

---

## 📦 Dependencies

Install all dependencies via:

```bash
pip install -r requirements.txt
```

Key packages used:
- **Flask** — Web framework
- **SQLite3** — Lightweight database (built-in with Python)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify it.

---

## 👤 Author

**2akj24**  
GitHub: [@2akj24](https://github.com/2akj24)

---

> 💪 *Stay consistent. Stay fit. Guruji has got your back.*
