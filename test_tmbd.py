import requests
url = "https://api.themoviedb.org/3/genre/movie/list?api_key=dc13ef2e032273cc2bc0a641ba0298ef"
res = requests.get(url, timeout=10)
print(res.status_code)
print(res.json())
