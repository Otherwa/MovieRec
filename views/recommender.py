import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# TMDb API key
API_KEY = os.getenv("API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_URL = "http://image.tmdb.org/t/p/w500/"


def calculate_num_ratings(dataset):
    """
    Calculate the number of ratings for each movie title in the dataset.

    Parameters:
    - dataset (pd.DataFrame): DataFrame containing movie ratings data.

    Returns:
    - pd.DataFrame: DataFrame containing movie titles and their corresponding number of ratings.
    """
    # Group by movie title and count the number of ratings
    num_ratings = dataset.groupby("title")["rating"].count()

    # Create a DataFrame with movie titles and number of ratings
    ratings = pd.DataFrame(num_ratings)
    ratings.columns = ["num of ratings"]  # Rename the column
    ratings["title"] = ratings.index  # Add 'title' column with movie titles

    return ratings


def movie_recommendation(movie_title, dataset, rate_count):
    """
    Recommends similar movies based on a selected movie title.

    Parameters:
    - movie_title (str): The title of the movie for which recommendations are needed.
    - dataset (pd.DataFrame): DataFrame containing movie ratings data.
    - rate_count (int): The minimum number of ratings required for a movie to be considered for recommendation.

    Returns:
    - pd.DataFrame: DataFrame containing top recommended movies along with their correlation scores.
    """
    # Create a pivot table of movie ratings
    moviemat = dataset.pivot_table(index="userId", columns="title", values="rating")

    # Get ratings for the selected movie
    selected_movie_ratings = moviemat[movie_title]

    # Calculate correlation with other movies
    similar_movies = moviemat.corrwith(selected_movie_ratings)

    # Create a DataFrame of correlations
    similar_movies = pd.DataFrame(similar_movies, columns=["Correlation"])

    # Drop NaN values
    similar_movies.dropna(inplace=True)

    # Calculate the number of ratings for each movie
    ratings = calculate_num_ratings(dataset)

    # Join with the number of ratings for each movie
    similar_movies = similar_movies.join(ratings["num of ratings"])

    similar_movies["title"] = similar_movies.index

    # Filter movies with a minimum number of ratings
    similar_movies = similar_movies[similar_movies["num of ratings"] > rate_count]

    # Sort by correlation
    similar_movies = similar_movies.sort_values("Correlation", ascending=False)

    return similar_movies.head(10)


def list_top_recommendations(rec_movies, dataset):
    """
    Lists top recommended movies with additional details.

    Parameters:
    - rec_movies (pd.DataFrame): DataFrame containing recommended movies.
    - dataset (pd.DataFrame): DataFrame containing additional movie data.

    Returns:
    - pd.DataFrame: DataFrame containing unique recommended movies with additional details.
    """
    # Merge recommended movies with the original dataset
    merged_dataset = pd.merge(rec_movies, dataset, on="title", how="left")

    merged_dataset.reset_index(inplace=True)

    # Grouping by 'title' column
    grouped_df = merged_dataset.groupby("title")

    # Getting only one row for each unique title
    unique_df = grouped_df.first().reset_index()

    unique_df.drop(columns=["userId"], inplace=True)

    return unique_df


def fetch_poster_url(movie_title):
    """
    Fetches the poster URL for a given movie title from TMDb API.

    Parameters:
    - movie_title (str): The title of the movie.

    Returns:
    - str: The URL of the movie poster.
    """
    params = {"api_key": API_KEY, "query": movie_title}
    response = requests.get(TMDB_API_URL, params=params).json()
    if response["results"]:
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return TMDB_IMAGE_URL + poster_path
    return None


def fetch_streaming_sites(movie_title):
    """
    Fetches streaming sites search results for a given movie title.

    Parameters:
    - movie_title (str): The title of the movie.

    Returns:
    - dict: A dictionary containing streaming sites and their respective URLs.
    """
    streaming_sites = {}

    # Perform search on Netflix
    netflix_url = f"https://www.netflix.com/search?q={movie_title}"
    streaming_sites["Netflix"] = netflix_url

    # Perform search on Amazon Prime
    amazon_url = f"https://www.primevideo.com/search?phrase={movie_title}"
    streaming_sites["Amazon Prime"] = amazon_url

    return streaming_sites
