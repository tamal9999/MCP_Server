from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Make sure your TMDb API key is set as an environment variable on Render
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

@app.route("/get_movies", methods=["GET"])
def get_movies():
    region = request.args.get("region", "IN")
    language = request.args.get("language", "en-IN")

    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "api_key": TMDB_API_KEY,
        "region": region,
        "language": language
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        movies = []
        for m in data.get("results", []):
            movies.append({
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "overview": m.get("overview"),
                "rating": m.get("vote_average"),
                "poster_path": m.get("poster_path")  # ✅ Added poster path
            })

        return jsonify(movies)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)