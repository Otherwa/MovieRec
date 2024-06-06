import streamlit as st
from views.howitworks import how_it_works
from views.recommender import (
    fetch_poster_url,
    list_top_recommendations,
    movie_recommendation,
)
import pandas as pd
import os

st.set_page_config(layout="wide")


def main():
    page = st.sidebar.radio("Navigation", ("Movie Recommendations", "How It Works"))

    # Get the current directory
    current_dir = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Construct the file path relative to the current directory
    file_path = os.path.join(current_dir, "./model/cleaned_dataset.csv")

    # Load the dataset
    dataset = pd.read_csv(file_path)

    if page == "Movie Recommendations":
        st.title("Movie Recommendation System")

        # Sidebar input for movie title and minimum rating count
        movie_titles = dataset["title"].unique().tolist()

        movie_title = st.selectbox("Enter a movie title", movie_titles)

        rate_count = st.slider(
            "Minimum number of ratings", min_value=0, max_value=500, value=100
        )

        # Button to trigger prediction
        if st.button("Get Recommendations"):
            # Get recommendations if data is loaded successfully
            recommendations = movie_recommendation(
                movie_title,
                dataset=dataset,
                rate_count=rate_count,
            )

            recommendations.reset_index(drop=True, inplace=True)

            top_list = list_top_recommendations(recommendations, dataset)

            # Display recommendations
            st.header("Top Recommendations")

            # Display top_list as a 3x*
            cols = st.columns(3)

            for index, row in top_list.iterrows():
                with cols[index % 3]:
                    # Fetch poster image URL
                    image = fetch_poster_url(row["title"])

                    # IMDb URL
                    imdb_url = f"https://www.imdb.com/find?q={row['title'].replace(' ', '+')}&s=tt"

                    # Add border around movie details
                    st.markdown(
                        f"""
                        <div style="display: flex; flex-direction: column; border: 2px solid #f0f0f0; border-radius: 10px; padding: 1.25rem; margin-bottom: 10px;">
                            {'<img src="' + image + '" style="width:100%; border-radius: 10px;" />' if image else ''}
                            <h3>{row["title"]}</h3>
                            <h6><a href="{imdb_url}" target="_blank" rel="noopener noreferrer">Reviews</a></h6>
                            <p><b>Rating:</b> {row['rating']}</p>
                            <p><b>Runtime:</b> {row['runtime']}</p>
                            <div style="max-height: 200px; overflow-y: auto;">
                                <p><b>Overview:</b></p>
                                <p style="margin-bottom: 0;">{row['overview']}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # data processed
            st.data_editor(top_list)

    elif page == "How It Works":
        how_it_works(dataset)


if __name__ == "__main__":
    main()
