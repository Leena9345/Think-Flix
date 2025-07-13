from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
import os, json
from dotenv import load_dotenv

from gemini import extract_movie_preferences, ask_watchlist_summary
from tmdb import get_genre_ids, search_movies_advanced, get_similar_movies
import auth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)

# MySQL config
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)
auth.init_mysql(mysql)

@app.route("/")
def home():
    if "user_id" in session:
        return render_template("query.html", username=session["username"])
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if auth.register_user(data["username"], data["password"]):
        return jsonify({"message": "Registered"})
    else:
        return jsonify({"error": "Username exists"}), 409

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user_id = auth.login_user(data["username"], data["password"])
    if user_id:
        session["user_id"] = user_id
        session["username"] = data["username"]
        return jsonify({"message": "Logged in"})
    else:
        return jsonify({"error": "Invalid"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/recommend-tmdb", methods=["POST"])
def recommend():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_input = request.json.get("query")
    print("User input:", user_input)

    raw = extract_movie_preferences(user_input)
    print("Gemini raw:", raw)

    clean = raw.strip().strip("```json").strip("```").strip()
    try:
        parsed = json.loads(clean)
    except Exception as e:
        print("Parse error:", e)
        return jsonify({"error": "Parse failed", "raw_output": raw})

    print("Parsed:", parsed)

    all_genres = get_genre_ids()
    matched_genre_ids = [all_genres[g] for g in parsed.get("genres", []) if g in all_genres]
    keywords = parsed.get("keywords", [])  # Gemini should output keywords too
    year_from = parsed.get("year_from", 2010)
    # Build lower-case mapping
    lower_genres = { k.lower(): v for k, v in all_genres.items() }
    matched_genre_ids = [ lower_genres[g.lower()] for g in parsed.get("genres", []) if g.lower() in lower_genres ]
    print("Gemini genres:", parsed.get("genres", []))
    print("TMDb all genres:", all_genres)
    print("Matched genre IDs:", matched_genre_ids)


    print("Genres:", matched_genre_ids, "Keywords:", keywords, "Year from:", year_from)

    movies = search_movies_advanced(genre_ids=matched_genre_ids)
    print("Fetched movies:", movies)

    results = [{"title": m["title"], "overview": m["overview"], "release_date": m["release_date"]} for m in movies]

    auth.save_history(session["user_id"], user_input, json.dumps(results))
    return jsonify({"query": user_input, "recommendations": results})


@app.route("/history")
def history():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    h = auth.get_user_history(session["user_id"])
    print("Fetched history:", h)
    return jsonify([{"query": q, "results": json.loads(r), "timestamp": str(t)} for q,r,t in h])

# app.py or wherever you define routes
from gemini import ask_watchlist_summary  # make sure this function exists

@app.route('/watchlist-explainer', methods=['POST'])
def watchlist_explainer():
    data = request.get_json()
    movie_titles = data.get('movies', '').split(',')
    movie_titles = [t.strip() for t in movie_titles if t.strip()]

    descriptions = []
    first_movie_id = None

    # Search TMDb to get overviews and first movie id
    from tmdb import search_tmdb_movie  # import if not already

    for title in movie_titles:
        meta = search_tmdb_movie(title)
        if meta:
            overview = meta.get('overview')
            if overview:
                descriptions.append(overview)
            if not first_movie_id:
                first_movie_id = meta.get('id')

    # Combine text to send to Gemini
    combined_text = " ".join(descriptions) if descriptions else ""

    summary = ask_watchlist_summary(combined_text) if combined_text else "Could not generate summary."

    # Get similar movies using TMDb recommendations
    similar = get_similar_movies(first_movie_id) if first_movie_id else []

    return jsonify({
        "summary": summary,
        "similar": [
            {"title": m["title"], "release_date": m["release_date"]}
            for m in similar
        ]
    })




if __name__ == "__main__":
    app.run(debug=True)
