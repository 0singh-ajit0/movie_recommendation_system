import streamlit as st
import pickle
import requests


movies_df = pickle.load(open("movies.pkl", "rb"))
movies_list = movies_df["title"].values
similarity_vecs = pickle.load(open("similarity_vecs.pkl", "rb"))


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=93e47aba56c74331ad7bea7f52f934d1")
    data = response.json()
    return "https://www.themoviedb.org/t/p/w500" + data["poster_path"]


def recommend(movie, count=5):
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity_vecs[movie_index]
    most_similar = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:(count+1)]

    most_similar_movies = []
    for movie in most_similar:
        cur_movie = movies_df.iloc[movie[0]]
        most_similar_movies.append((cur_movie["movie_id"], cur_movie["title"], fetch_poster(cur_movie["movie_id"])))
    return most_similar_movies


st.title("Movie Recommender System")
option = st.selectbox(
    'Select a movie',
    movies_list,
    index=None,
    placeholder="Select a movie"
)

if st.button("Recommend"):
    recommendations = recommend(option)
    cols = st.columns(5)

    for i, movie in enumerate(recommendations):
        with cols[i]:
            st.header(movie[1])
            st.image(movie[2])
