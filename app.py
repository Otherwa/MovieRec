import streamlit as st
from views.howitworks import how_it_works
from views.recommender import list_top_recommendations, movie_recommendation
import pandas as pd


def main():
    page = st.sidebar.radio("Navigation", ("Movie Recommendations", "How It Works"))

    dataset = pd.read_csv(
        r"C:\Users\athar\OneDrive\Desktop\DEV\MovieRec\model\cleaned_dataset.csv"
    )

    if page == "Movie Recommendations":
        st.title("Movie Recommendation System")

        # Sidebar input for movie title and minimum rating count
        movie_title = st.text_input("Enter a movie title", "Back to the Future Part II")
        rate_count = st.slider(
            "Minimum number of ratings", min_value=0, max_value=500, value=100
        )

        # Button to trigger prediction
        if st.button("Predict"):
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

            # Display top_list as a 3x4 grid
            cols = st.columns(2)

            for index, row in top_list.iterrows():
                with cols[index % 2]:
                    st.subheader(row["title"])
                    st.write(f"Rating:\n {row['rating']}")
                    st.write(f"Runtime:\n {row['runtime']}")
                    st.write(f"Overview:\n {row['overview']}")

    elif page == "How It Works":
        how_it_works()


if __name__ == "__main__":
    main()
