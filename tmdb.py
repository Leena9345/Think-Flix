# backend/tmdb.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def get_genre_ids():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    res = requests.get(url)
    data = res.json()
    genres = { g["name"]: g["id"] for g in data["genres"] }
    print("Fetched genres:", genres)
    return genres


def search_movies_advanced(genre_ids=None):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=popularity.desc"

    if genre_ids:
        url += "&with_genres=" + ",".join(str(g) for g in genre_ids)

    print("Final TMDb URL:", url)
    res = requests.get(url)
    data = res.json()
    print("TMDb raw response:", data)
    return data.get("results", [])[:10]

def get_similar_movies(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params)
    data = res.json()
    return data.get("results", [])[:5]

def search_tmdb_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    res = requests.get(url, params=params)
    data = res.json()
    return data["results"][0] if data.get("results") else None
