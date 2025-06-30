from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model
class SuggestionRequest(BaseModel):
    input: str

# DB init
conn = sqlite3.connect('food_suggestions.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    suggestion TEXT,
    timestamp TEXT
)
''')
conn.commit()

# Dummy suggestion logic
suggestion_map = {
    "happy": ["Ice Cream", "Pizza", "Burger"],
    "sad": ["Chocolate", "Soup", "Comfort Food"],
    "spicy": ["Biryani", "Tacos", "Spicy Ramen"],
    "sweet": ["Cake", "Donuts", "Gulab Jamun"],
    "tired": ["Coffee", "Protein Bar", "Energy Drink"],
}

@app.post("/suggest")
def get_food_suggestion(req: SuggestionRequest):
    user_input = req.input.lower()
    suggestion = "How about a salad or something refreshing? 🥗"
    
    for keyword in suggestion_map:
        if keyword in user_input:
            suggestion = f"Try some {suggestion_map[keyword][0]} 🍽️"
            break

    # Store in database
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO suggestions (user_input, suggestion, timestamp) VALUES (?, ?, ?)",
        (req.input, suggestion, timestamp)
    )
    conn.commit()

    return {"suggestion": suggestion}
