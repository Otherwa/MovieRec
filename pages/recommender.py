import streamlit as st
import pandas as pd
import pickle
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the pickle files
movie_recommendation_path = os.path.join(
    current_dir, "../model/movie_recommendation_v1.0.pkl"
)
list_top_recommendation_path = os.path.join(
    current_dir, "../model/movie_recommendation_lister_v1.0.pkl"
)

# Load the movie recommendation function from the pickle file
with open(movie_recommendation_path, "rb") as f:
    movie_recommendation = pickle.load(f)

# Load the movie recommendation function from the pickle file
with open(list_top_recommendation_path, "rb") as f:
    list_top_recommendation = pickle.load(f)

# Load the datasets
movies = pd.read_csv("movies_metadata.csv")
ratings = pd.read_csv("ratings.csv")


# Main function to recommend movies
def recommend_movies(movie_title, rate_count):
    dataset = pd.merge(movies, ratings, how="right", on="movieId")
    recommendations = movie_recommendation(movie_title, dataset, rate_count)
    recommendations.reset_index(drop=True, inplace=True)
    recommendations = list_top_recommendation(recommendations, dataset)
    return recommendations


def main():
    st.title("Movie Recommendation System")

    # Sidebar input for movie title and minimum rating count
    movie_title = st.text_input("Enter a movie title", "Back to the Future Part II")
    rate_count = st.slider(
        "Minimum number of ratings", min_value=0, max_value=500, value=100
    )

    # Get recommendations
    recommendations = recommend_movies(movie_title, rate_count)

    # Display recommendations
    st.header("Top Recommendations")
    st.dataframe(recommendations)


if __name__ == "__main__":
    main()
