import random
import json

# Dateiname zur Speicherung der Daten
DATA_FILE = "movies.json"

def get_movies():
    """
    Lädt die Filmdaten aus einer JSON-Datei und gibt sie als Dictionary zurück.
    Falls die Datei nicht existiert, wird ein leeres Dictionary zurückgegeben.
    """
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Fehler: Die Datei ist beschädigt. Sie wird zurückgesetzt.")
        return {}

def save_movies(movies):
    """
    Speichert die Filmdaten in einer JSON-Datei.
    Args:
        movies (dict): Das Dictionary der Filme.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(movies, file, indent=4)
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")

def list_movies():
    """
    Listet alle Filme mit Titel, Bewertung und Erscheinungsjahr auf.
    """
    movies = get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    print(f"{len(movies)} Filme insgesamt:")
    for title, details in movies.items():
        print(f"{title} ({details['year']}): {details['rating']}")

def add_movie():
    """
    Fügt einen neuen Film mit Titel, Erscheinungsjahr und Bewertung hinzu.
    """
    title = input("Titel des Films: ")
    try:
        year = int(input("Erscheinungsjahr: "))
        rating = float(input("Bewertung (0-10): "))
        if not (0 <= rating <= 10):
            print("Fehler: Die Bewertung muss zwischen 0 und 10 liegen.")
            return
    except ValueError:
        print("Fehler: Ungültiges Erscheinungsjahr oder Bewertung.")
        return

    movies = get_movies()
    if title in movies:
        print(f"Der Film '{title}' existiert bereits in der Datenbank.")
        return

    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)
    print(f"Film '{title}' erfolgreich hinzugefügt!")

def delete_movie():
    """
    Löscht einen Film aus der Datenbank.
    """
    title = input("Titel des zu löschenden Films: ")
    movies = get_movies()
    if title not in movies:
        print(f"Fehler: Film '{title}' nicht gefunden.")
        return

    del movies[title]
    save_movies(movies)
    print(f"Film '{title}' erfolgreich gelöscht!")

def update_movie():
    """
    Aktualisiert die Bewertung eines Films in der Datenbank.
    """
    title = input("Titel des zu aktualisierenden Films: ")
    movies = get_movies()
    if title not in movies:
        print(f"Fehler: Film '{title}' nicht gefunden.")
        return

    try:
        rating = float(input("Neue Bewertung (0-10): "))
        if not (0 <= rating <= 10):
            print("Fehler: Die Bewertung muss zwischen 0 und 10 liegen.")
            return
    except ValueError:
        print("Fehler: Ungültige Bewertung.")
        return

    movies[title]["rating"] = rating
    save_movies(movies)
    print(f"Film '{title}' erfolgreich aktualisiert!")

def stats():
    """
    Zeigt Statistiken zu den Filmen an, einschließlich Durchschnittsbewertung,
    Medianbewertung, bester und schlechtester Film.
    """
    movies = get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    ratings = [details["rating"] for details in movies.values()]
    average = sum(ratings) / len(ratings)
    median = sorted(ratings)[len(ratings) // 2] if len(ratings) % 2 != 0 else sum(sorted(ratings)[len(ratings)//2-1:len(ratings)//2+1]) / 2
    best_rating = max(ratings)
    worst_rating = min(ratings)

    best_movies = [title for title, details in movies.items() if details["rating"] == best_rating]
    worst_movies = [title for title, details in movies.items() if details["rating"] == worst_rating]

    print(f"Durchschnittliche Bewertung: {average:.1f}")
    print(f"Median der Bewertungen: {median}")
    print("Bester Film(e):", ", ".join(best_movies))
    print("Schlechtester Film(e):", ", ".join(worst_movies))

def search_movie():
    """
    Durchsucht die Filme nach einem Teil des Titels (Groß-/Kleinschreibung ignoriert).
    """
    query = input("Suchbegriff: ")
    movies = get_movies()
    matches = {title: details for title, details in movies.items() if query.lower() in title.lower()}

    if matches:
        for title, details in matches.items():
            print(f"{title} ({details['year']}): {details['rating']}")
    else:
        print("Keine Filme gefunden.")

def movies_sorted_by_rating():
    """
    Zeigt die Filme sortiert nach ihrer Bewertung in absteigender Reihenfolge.
    """
    movies = get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
    for title, details in sorted_movies:
        print(f"{title} ({details['year']}): {details['rating']}")

def random_movie():
    """
    Gibt einen zufällig ausgewählten Film und dessen Bewertung aus.
    Gibt eine Meldung aus, wenn keine Filme in der Datenbank sind.
    """
    movies = get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    name, rating = random.choice(list(movies.items()))
    print(f"Zufälliger Film: {name}, {rating}")

def main():
    """
    Hauptfunktion, die ein Menü anzeigt und die entsprechenden Befehle ausführt.
    Ermöglicht dem Benutzer, zwischen verschiedenen Optionen zu wählen.
    """
    menu = {
        '1': ("Filme anzeigen", list_movies),
        '2': ("Film hinzufügen", add_movie),
        '3': ("Film löschen", delete_movie),
        '4': ("Film aktualisieren", update_movie),
        '5': ("Statistiken", stats),
        '6': ("Zufälliger Film", random_movie),
        '7': ("Filme suchen", search_movie),
        '8': ("Filme nach Bewertung sortieren", movies_sorted_by_rating),
        '9': ("Beenden", None)
    }

    while True:
        print("\n********** My Movies Database **********")
        print("Menü:")
        for key, (description, _) in menu.items():
            print(f"{key}. {description}")
        try:
            choice = input("Wähle eine Option (1-9): ")

            if choice == '9':
                print("Auf Wiedersehen!")
                break

            action = menu.get(choice)
            if action:
                _, func = action
                func()
            else:
                print("Ungültige Auswahl, bitte erneut versuchen.")
        except EOFError:
            print("Eingabefehler: Keine Eingabe verfügbar.")
            break

if __name__ == "__main__":
    main()
# Copy your code from the previous Movies project