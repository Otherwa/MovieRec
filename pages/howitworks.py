import streamlit as st


def how_it_works():
    st.title("How It Works")

    st.markdown("This page explains how our movie recommendation system functions.")

    st.header("1. Data Loading and Exploration")
    st.markdown(
        """
    - The system loads movie metadata and ratings data.
    - It explores the datasets to understand their structure and content.
    """
    )

    st.header("2. Genre and Title Lists")
    st.markdown(
        """
    - Unique genres and movie titles are extracted from the movies dataset.
    - They are stored for further use.
    """
    )

    st.header("3. Movie Ratings Analysis")
    st.markdown(
        """
    - Movies are analyzed based on their average ratings and the number of ratings received.
    - Visualizations like heatmaps and joint plots help explore relationships between ratings and the number of ratings.
    """
    )

    st.header("4. Movie Recommendation Function")
    st.markdown(
        """
    - A function called `movie_recommendation()` recommends similar movies based on user ratings.
    - It calculates correlations between the selected movie and others.
    - Movies with a minimum number of ratings are filtered out.
    - Top recommended movies based on correlation are returned.
    """
    )

    st.header("5. Top Recommendations Listing Function")
    st.markdown(
        """
    - Another function called `list_top_recommendations()` lists top recommendations with additional details.
    - It merges recommended movies with the original dataset to get additional information.
    - Unnecessary columns are removed, and only unique recommendations are returned.
    """
    )

    st.header("6. Pickle File Usage")
    st.markdown(
        """
    - The recommendation functions are saved into pickle files for later use.
    """
    )

    st.header("7. Loading Pickle Files")
    st.markdown(
        """
    - Pickle files containing the recommendation functions are loaded when needed.
    """
    )

    st.header("8. Using Recommendation Functions")
    st.markdown(
        """
    - Users can specify a movie title for which recommendations are needed.
    - The recommendation functions are called to get recommendations based on the specified movie title.
    """
    )


if __name__ == "__main__":
    how_it_works()
