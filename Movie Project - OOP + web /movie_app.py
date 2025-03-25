import requests
import random
import os
import shutil
from movie_storage import list_movies, add_movie, delete_movie, update_movie


class MovieApp:
    def __init__(self):
        """Initialisiert die MovieApp."""
        self._api_key = "YOUR_API_KEY"  # Ersetze dies mit deinem OMDb API-Schlüssel
        self._template_dir = "static"

    def _fetch_movie_data(self, title: str) -> dict | None:
        """
        Ruft Filmdaten von der OMDb API ab.
        """
        url = f"http://www.omdbapi.com/?apikey={self._api_key}&t={title}"
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

    def _command_list_movies(self):
        """Listet alle Filme in der Datenbank auf."""
        movies = list_movies()
        if not movies:
            print("Keine Filme in der Datenbank.")
        else:
            for title, details in movies.items():
                print(f"{title} ({details['year']}): Rating {details['rating']}, Poster: {details['poster']}")

    def _command_add_movie(self):
        """Fügt einen neuen Film zur Datenbank hinzu, indem die OMDb API verwendet wird."""
        title = input("Film-Titel eingeben: ").strip()
        if not title:
            print("Fehler: Bitte gib einen gültigen Titel ein.")
            return
        movie_data = self._fetch_movie_data(title)
        if movie_data:
            add_movie(
                movie_data["title"],
                movie_data["year"],
                movie_data["rating"],
                movie_data["poster"]
            )
            print(f"{movie_data['title']} wurde hinzugefügt.")
        else:
            print("Film konnte nicht hinzugefügt werden.")

    def _command_delete_movie(self):
        """Löscht einen Film aus der Datenbank."""
        title = input("Zu löschenden Film-Titel eingeben: ").strip()
        movies = list_movies()
        if title in movies:
            delete_movie(title)
            print(f"{title} wurde gelöscht.")
        else:
            print("Film nicht gefunden.")

    def _command_update_movie(self):
        """Aktualisiert die Bewertung eines Films."""
        title = input("Zu aktualisierenden Film-Titel eingeben: ").strip()
        movies = list_movies()
        if title in movies:
            try:
                rating = float(input("Neue Bewertung eingeben (0-10): "))
                update_movie(title, rating)
                print(f"Bewertung von {title} wurde aktualisiert.")
            except ValueError:
                print("Ungültige Bewertung.")
        else:
            print("Film nicht gefunden.")

    def _command_stats(self):
        """Zeigt Statistiken über die Filme an."""
        movies = list_movies()
        if not movies:
            print("Keine Filme für Statistiken verfügbar.")
            return
        total_movies = len(movies)
        avg_rating = sum(float(movie["rating"]) for movie in movies.values()) / total_movies
        top_movie = max(movies.items(), key=lambda x: x[1]["rating"])
        print(f"Anzahl Filme: {total_movies}")
        print(f"Durchschnittliche Bewertung: {avg_rating:.2f}")
        print(f"Am besten bewerteter Film: {top_movie[0]} ({top_movie[1]['rating']})")

    def _command_random_movie(self):
        """Zeigt einen zufälligen Film aus der Datenbank an."""
        movies = list_movies()
        if not movies:
            print("Keine Filme in der Datenbank.")
            return
        random_title = random.choice(list(movies.keys()))
        details = movies[random_title]
        print(f"Zufälliger Film: {random_title} ({details['year']}): Rating {details['rating']}")

    def _command_search_movie(self):
        """Sucht nach einem Film anhand des Titels."""
        search_term = input("Suchbegriff eingeben: ").strip().lower()
        movies = list_movies()
        found = False
        for title, details in movies.items():
            if search_term in title.lower():
                print(f"{title} ({details['year']}): Rating {details['rating']}")
                found = True
        if not found:
            print("Keine Filme gefunden.")

    def _command_sort_by_rating(self):
        """Listet Filme sortiert nach Bewertung (absteigend)."""
        movies = list_movies()
        if not movies:
            print("Keine Filme in der Datenbank.")
            return
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        for title, details in sorted_movies:
            print(f"{title} ({details['year']}): Rating {details['rating']}")

    def _generate_website(self):
        """Generiert die Website basierend auf der Vorlage."""
        movies = list_movies()
        if not movies:
            print("Keine Filme zum Generieren der Website verfügbar.")
            return
        template_path = os.path.join(self._template_dir, "index_template.html")
        if not os.path.exists(template_path):
            print("Fehler: Template-Datei nicht gefunden.")
            return
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        movie_grid = ""
        for title, details in movies.items():
            movie_grid += f"""
            <div class="movie-item">
                <img src="{details['poster']}" alt="{title} Poster" onerror="this.src='https://via.placeholder.com/200'">
                <h3>{title}</h3>
                <p>Jahr: {details['year']}</p>
                <p>Bewertung: {details['rating']}</p>
            </div>
"""
        html_content = template.replace("__TEMPLATE_TITLE__", "Meine Filmesammlung")
        html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        css_source = os.path.join(self._template_dir, "style.css")
        if os.path.exists(css_source):
            shutil.copy(css_source, "style.css")
        else:
            print("Warnung: style.css nicht gefunden, Styling könnte fehlen.")
        print("Website was generated successfully.")

    def run(self):
        """Startet die interaktive Menüschleife der Anwendung."""
        while True:
            print("\n********** My Movies Database **********")
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")

            choice = input("Wähle eine Option (0-9): ").strip()

            if choice == "0":
                print("Auf Wiedersehen!")
                break
            elif choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sort_by_rating()
            elif choice == "9":
                self._generate_website()
            else:
                print("Ungültige Eingabe, bitte erneut versuchen.")