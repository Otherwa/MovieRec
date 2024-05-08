import streamlit as st
from pages.howitworks import how_it_works
from pages.recommender import recommend_movies


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Movie Recommendations", "How It Works"))

    if page == "Movie Recommendations":
        st.title("Movie Recommendation System")
        movie_title = st.text_input("Enter a movie title", "Back to the Future Part II")
        rate_count = st.slider(
            "Minimum number of ratings", min_value=0, max_value=500, value=100
        )
        recommendations = recommend_movies(movie_title, rate_count)
        st.header("Top Recommendations")
        st.dataframe(recommendations)

    elif page == "How It Works":
        how_it_works()


if __name__ == "__main__":
    main()
