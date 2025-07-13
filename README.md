# Think-Flix
🎬 ThinkFlix – Smart Movie Recommender
ThinkFlix is an AI-powered movie recommender web application that interprets natural language input to suggest personalized movie recommendations using Gemini API and TMDb API.

“Thoughtful movie suggestions powered by natural language understanding.”

🌟 Features

✅ Freeform movie search:
Users can type what they feel like watching (e.g., “funny animated movie under 2 hours”). Gemini extracts genres & preferences, and TMDb recommends matching movies.

✅ User login & search history:
Users can register, log in, and view past searches and recommendations.

✅ Watchlist explainer:
Enter favorite movies (e.g., Inception, Interstellar) and Gemini summarizes your viewing taste, plus TMDb suggests similar movies.

🛠️ Tech Stack
Backend: Python (Flask)

Frontend: HTML, CSS, JavaScript

AI Integration: Gemini API (Google)

Movie Data: TMDb API

Database: MySQL

🔄 Workflow & How it works

User enters a natural language movie request.

Gemini interprets the input → extracts genres, moods, and keywords.

These are mapped to TMDb’s genre IDs.

App queries TMDb’s Discover Movies API → fetches movies.

Results (title, year, overview) are shown on screen.

User’s query & recommendations are saved to their search history.

(Optional) Watchlist Explainer: user enters favorite movies → Gemini summarizes their taste + TMDb recommends similar movies.

▶️ Running the App

python app.py
Then open: http://127.0.0.1:5000

✨ Project Highlights

Uses AI + real-time APIs to create a natural movie discovery experience.

Clean, dark-themed UI inspired by popular streaming platforms.

Search history and watchlist features for personalization.

📌 Project Name Meaning

ThinkFlix → Thoughtful suggestions of movies, powered by Gemini’s natural language understanding.
