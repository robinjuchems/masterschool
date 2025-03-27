from storage.storage_sqlalchemy import StorageSqlAlchemy

# Globale Instanz der Speicherklasse
_storage = StorageSqlAlchemy("data/movies.db")

def list_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    The function loads the information from the database and returns the data.
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
    return _storage.list_movies()

def add_movie(title, year, rating, poster=None):
    """
    Adds a movie to the movies database.
    Adds the movie to the database.
    The function doesn't need to validate the input.
    """
    _storage.add_movie(title, year, rating, poster)

def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Deletes the movie from the database.
    The function doesn't need to validate the input.
    """
    _storage.delete_movie(title)

def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Updates the movie in the database.
    The function doesn't need to validate the input.
    """
    _storage.update_movie(title, rating)