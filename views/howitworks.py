import streamlit as st
from views.recommender import *


def how_it_works(dataset):
    st.title("How It Works")

    st.markdown("This page explains how our movie recommendation system functions.")

    steps = [
        (
            "Data Loading and Exploration",
            "The system loads and explores movie metadata and ratings data.",
        ),
        (
            "Genre and Title Lists",
            "Unique genres and movie titles are extracted and stored.",
        ),
        (
            "Movie Ratings Analysis",
            "Movies are analyzed based on average ratings and the number of ratings received.",
        ),
        (
            "Movie Recommendation Function",
            "A function recommends similar movies based on user ratings.",
        ),
        (
            "Top Recommendations Listing Function",
            "Another function lists top recommendations with additional details.",
        ),
        (
            "Using Recommendation Functions",
            "Users can specify a movie title for recommendations.",
        ),
    ]

    for step, description in steps:
        st.header(step)
        st.markdown(description)

    st.dataframe(dataset)

    st.markdown("**Functions Used:**")
    st.markdown(
        "- `calculate_num_ratings()`: Calculates the number of ratings for each movie title."
    )
    st.write(calculate_num_ratings)
    st.markdown(
        "- `movie_recommendation()`: Recommends similar movies based on user ratings."
    )
    st.write(movie_recommendation)
    st.markdown(
        "- `list_top_recommendations()`: Lists top recommendations with additional details."
    )
    st.write(list_top_recommendations)
    st.markdown(
        "- `fetch_poster_url()`: Fetches the poster URL for a given movie title from the TMDb API."
    )
    st.write(fetch_poster_url)


if __name__ == "__main__":
    how_it_works()
