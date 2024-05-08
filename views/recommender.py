import streamlit as st
import pandas as pd
import os


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

    merged_dataset = pd.merge(rec_movies, dataset, on="title", how="left")

    merged_dataset.reset_index(inplace=True)

    # Grouping by 'title' column
    grouped_df = merged_dataset.groupby("title")

    # Getting only one row for each unique title
    unique_df = grouped_df.first().reset_index()

    unique_df.drop(columns=["userId"], inplace=True)

    return unique_df
