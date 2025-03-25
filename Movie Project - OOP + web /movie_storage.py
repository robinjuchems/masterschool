import json
import os

# Globale Variable für die Speicherdatei
FILE_PATH = "movies.json"

def list_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    The function loads the information from the JSON file and returns the data.
    For example:
    {
        "Titanic": {
            "rating": 9,
            "year": 1999
        },
        "...": {
            ...
        }
    }
    """
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, 'r') as f:
        return json.load(f)

def add_movie(title, year, rating, poster=None):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, adds the movie, and saves it.
    The function doesn't need to validate the input.
    """
    movies = list_movies()
    movies[title] = {
        "year": year,
        "rating": rating,
        "poster": poster if poster is not None else "N/A"
    }
    with open(FILE_PATH, 'w') as f:
        json.dump(movies, f, indent=4)

def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie, and saves it.
    The function doesn't need to validate the input.
    """
    movies = list_movies()
    if title in movies:
        del movies[title]
        with open(FILE_PATH, 'w') as f:
            json.dump(movies, f, indent=4)

def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie, and saves it.
    The function doesn't need to validate the input.
    """
    movies = list_movies()
    if title in movies:
        movies[title]["rating"] = rating
        with open(FILE_PATH, 'w') as f:
            json.dump(movies, f, indent=4)