import os
import requests
from dotenv import load_dotenv
import json
import re

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_movie_preferences(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
Extract structured JSON:
{{
  "genres": [ genre names ],
  "keywords": [ mood words or themes ],
  "year_from": 2010
}}
from: '{user_input}'
Return only JSON.
"""
            }]
        }]
    }
    res = requests.post(url, json=payload)
    data = res.json()
    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    clean = raw_text.strip().strip("```json").strip("```").strip()
    return clean

def ask_watchlist_summary(movies):
    prompt = f"""Given this list of movies: {movies}, write a short personality-style summary 
describing what this says about the user's taste. Keep it short and relevant to the genres."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    res = requests.post(url, json=payload)
    data = res.json()
    print("Gemini raw response:", json.dumps(data, indent=2))  # ✅ debug print
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Gemini parse error:", e)
        return "Could not generate summary."
