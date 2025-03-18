import json
import random

DATA_FILE = "movies.json"

def get_movies():
    """
    Lädt die Filmdaten aus der JSON-Datei und gibt sie als Dictionary zurück.
    Falls die Datei nicht existiert oder beschädigt ist, wird ein leeres Dictionary zurückgegeben.
    """
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_movies(movies):
    """
    Speichert die Filmdaten in der JSON-Datei.
    Args:
        movies (dict): Das Dictionary der Filme.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(movies, file, indent=4)
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")

def add_movie(title, year, rating):
    """
    Fügt einen neuen Film hinzu, wenn er noch nicht existiert.
    Args:
        title (str): Titel des Films
        year (int): Erscheinungsjahr
        rating (float): Bewertung (0-10)
    Returns:
        bool: True, wenn erfolgreich, False, wenn der Film bereits existiert
    """
    movies = get_movies()
    if title in movies:
        return False
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)
    return True

def delete_movie(title):
    """
    Löscht einen Film aus der Datenbank.
    Args:
        title (str): Titel des Films
    Returns:
        bool: True, wenn erfolgreich, False, wenn der Film nicht gefunden wurde
    """
    movies = get_movies()
    if title not in movies:
        return False
    del movies[title]
    save_movies(movies)
    return True

def update_movie(title, new_rating):
    """
    Aktualisiert die Bewertung eines Films.
    Args:
        title (str): Titel des Films
        new_rating (float): Neue Bewertung (0-10)
    Returns:
        bool: True, wenn erfolgreich, False, wenn der Film nicht gefunden wurde
    """
    movies = get_movies()
    if title not in movies:
        return False
    movies[title]["rating"] = new_rating
    save_movies(movies)
    return True

def get_stats():
    """
    Berechnet Statistiken zu den Filmen.
    Returns:
        dict: Statistiken (Durchschnitt, Median, beste/schlechteste Filme) oder None, wenn keine Filme
    """
    movies = get_movies()
    if not movies:
        return None
    ratings = [details["rating"] for details in movies.values()]
    average = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    median = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 != 0 else (sorted_ratings[len(ratings)//2 - 1] + sorted_ratings[len(ratings)//2]) / 2
    best_rating = max(ratings)
    worst_rating = min(ratings)
    best_movies = [title for title, details in movies.items() if details["rating"] == best_rating]
    worst_movies = [title for title, details in movies.items() if details["rating"] == worst_rating]
    return {
        "average": average,
        "median": median,
        "best_movies": best_movies,
        "worst_movies": worst_movies
    }

def search_movie(query):
    """
    Sucht nach Filmen, deren Titel den Suchbegriff enthalten.
    Args:
        query (str): Suchbegriff
    Returns:
        dict: Gefundene Filme
    """
    movies = get_movies()
    return {title: details for title, details in movies.items() if query.lower() in title.lower()}

def get_sorted_movies():
    """
    Gibt die Filme nach Bewertung sortiert (absteigend) zurück.
    Returns:
        list: Sortierte Liste von (Titel, Details)-Tupeln
    """
    movies = get_movies()
    return sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)

def get_random_movie():
    """
    Gibt einen zufälligen Film zurück.
    Returns:
        tuple: (Titel, Details) oder None, wenn keine Filme
    """
    movies = get_movies()
    if not movies:
        return None
    return random.choice(list(movies.items()))