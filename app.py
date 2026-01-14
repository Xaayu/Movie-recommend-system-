from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# LOAD DATA (use your existing files)
movies = pickle.load(open("movies_df.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie):
    movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]
    distances = list(enumerate(similarity[movie_index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    rec = []
    for i in distances[1:6]:
        rec.append(movies.iloc[i[0]]['title'])

    return rec


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend_api():
    data = request.get_json()
    movie = data.get("movie")

    try:
        recommendations = recommend(movie)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)