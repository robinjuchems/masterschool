import json
import os
import requests


class MovieApp:
    def __init__(self, file_path="movies.json"):
        self.file_path = file_path
        self.api_key = "YOUR_API_KEY"  # Ersetze mit deinem OMDb API-Schlüssel
        self.movies = self._load_movies()

    def _load_movies(self):
        """Lädt die Filmdaten aus der JSON-Datei."""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_movies(self):
        """Speichert die Filmdaten in die JSON-Datei."""
        with open(self.file_path, 'w') as f:
            json.dump(self.movies, f, indent=4)

    def _fetch_movie_data(self, title):
        """Ruft Filmdaten von der OMDb API ab."""
        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("Response") == "True":
                return {
                    "title": data["Title"],
                    "year": int(data["Year"]),
                    "rating": float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0,
                    "poster": data.get("Poster", "N/A")
                }
            else:
                print(f"Fehler: {data.get('Error', 'Film nicht gefunden')}")
                return None
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return None

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        The function loads the information from the JSON file and returns the data.
        For example:
        {
            "Titanic": {
                "rating": 9,
                "year": 1999
            }
        }
        """
        return self.movies

    def add_movie(self, title, year=None, rating=None):
        """
        Adds a movie to the movies database.
        If only title is provided, it fetches data from the OMDb API.
        If title, year, and rating are provided, it adds the movie manually.
        """
        if year is None and rating is None:
            # API-Modus
            movie_data = self._fetch_movie_data(title)
            if movie_data:
                self.movies[movie_data["title"]] = {
                    "year": movie_data["year"],
                    "rating": movie_data["rating"],
                    "poster": movie_data["poster"]
                }
                self._save_movies()
                print(f"{movie_data['title']} wurde hinzugefügt.")
            else:
                print("Film konnte nicht hinzugefügt werden.")
        else:
            # Manueller Modus (mindestens title, year, rating erforderlich)
            self.movies[title] = {
                "year": year,
                "rating": rating,
                "poster": "N/A"  # Standardwert, da nicht erforderlich
            }
            self._save_movies()
            print(f"{title} wurde manuell hinzugefügt.")

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie, and saves it.
        """
        if title in self.movies:
            del self.movies[title]
            self._save_movies()
            print(f"{title} wurde gelöscht.")
        else:
            print("Film nicht gefunden.")

    def update_movie(self, title, rating):
        """
        Updates a movie in the movies database.
        Loads the information from the JSON file, updates the movie, and saves it.
        """
        if title in self.movies:
            self.movies[title]["rating"] = rating
            self._save_movies()
            print(f"Bewertung von {title} wurde aktualisiert.")
        else:
            print("Film nicht gefunden.")

    def run(self):
        """Startet die interaktive Menüschleife der Anwendung."""
        while True:
            print("\n=== Movies App Menu ===")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie (via API)")
            print("3. Add movie (manual)")
            print("4. Delete movie")
            print("5. Update movie")

            choice = input("Wähle eine Option (0-5): ").strip()

            if choice == "0":
                print("Auf Wiedersehen!")
                break
            elif choice == "1":
                movies = self.list_movies()
                if not movies:
                    print("Keine Filme in der Datenbank.")
                else:
                    for title, details in movies.items():
                        print(f"{title} ({details['year']}): Rating {details['rating']}")
            elif choice == "2":
                title = input("Film-Titel eingeben: ").strip()
                self.add_movie(title)
            elif choice == "3":
                title = input("Film-Titel eingeben: ").strip()
                try:
                    year = int(input("Erscheinungsjahr eingeben: "))
                    rating = float(input("Bewertung eingeben (0-10): "))
                    self.add_movie(title, year, rating)
                except ValueError:
                    print("Ungültige Eingabe für Jahr oder Bewertung.")
            elif choice == "4":
                title = input("Zu löschenden Film-Titel eingeben: ").strip()
                self.delete_movie(title)
            elif choice == "5":
                title = input("Zu aktualisierenden Film-Titel eingeben: ").strip()
                try:
                    rating = float(input("Neue Bewertung eingeben (0-10): "))
                    self.update_movie(title, rating)
                except ValueError:
                    print("Ungültige Bewertung.")
            else:
                print("Ungültige Eingabe, bitte erneut versuchen.")


if __name__ == "__main__":
    app = MovieApp()
    app.run()