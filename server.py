from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual TMDb API key for quick testing
API_KEY = "8b07f51b42dbee3708cde0a37152ab11"

@app.route("/get_movies", methods=["GET"])
def get_movies():
    # Default: India (IN)
    region = request.args.get("region", "IN")
    language = request.args.get("language", "en-IN")

    url = f"https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "api_key": API_KEY,
        "region": region,
        "language": language,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    movies = []
    if "results" in data:
        for m in data["results"][:5]:  # Limit to 5 results
            movies.append({
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "overview": m.get("overview"),
                "rating": m.get("vote_average")
            })

    return jsonify(movies)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)