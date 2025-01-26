import random
import statistics

# Dictionary to store movies and ratings
# dieses Dictionary speichert die Filme als Schlüssel und deren Bewertungen als Werte
movies = {
    "The Shawshank Redemption": 9.5,
    "Pulp Fiction": 8.8,
    "The Room": 3.6,
    "The Godfather": 9.2,
    "The Godfather: Part II": 9.0,
    "The Dark Knight": 9.0,
    "12 Angry Men": 8.9,
    "Everything Everywhere All At Once": 8.9,
    "Forrest Gump": 8.8,
    "Star Wars: Episode V": 8.7
}

def list_movies():
    """
    Zeigt alle Filme und deren Bewertungen an.
    Gibt auch die Gesamtanzahl der Filme in der Datenbank aus.
    """
    print(f"{len(movies)} Filme insgesamt")
    for movie, rating in movies.items():
        print(f"{movie}: {rating}")

def add_movie():
    """
    Fügt einen neuen Film und dessen Bewertung dem Dictionary hinzu.
    Verhindert das Hinzufügen eines bereits existierenden Films.
    """
    try:
        name = input("Gib den Namen des Films ein: ")
        if name in movies:
            print("Fehler: Film existiert bereits!")
            return
        rating = float(input("Gib die Bewertung des Films ein: "))
        movies[name] = rating
        print(f"Film '{name}' erfolgreich hinzugefügt!")
    except ValueError:
        print("Ungültige Bewertung. Bitte eine Zahl eingeben.")

def delete_movie():
    """
    Löscht einen Film aus dem Dictionary anhand seines Namens.
    Gibt eine Fehlermeldung aus, wenn der Film nicht gefunden wird.
    """
    try:
        name = input("Gib den Namen des zu löschenden Films ein: ")
        if name in movies:
            del movies[name]
            print(f"Film '{name}' erfolgreich gelöscht!")
        else:
            print("Fehler: Film nicht gefunden!")
    except EOFError:
        print("Eingabefehler: Keine Eingabe verfügbar.")

def update_movie():
    """
    Aktualisiert die Bewertung eines vorhandenen Films.
    Gibt eine Fehlermeldung aus, wenn der Film nicht existiert.
    """
    try:
        name = input("Gib den Namen des zu aktualisierenden Films ein: ")
        if name in movies:
            new_rating = float(input("Gib die neue Bewertung ein: "))
            movies[name] = new_rating
            print(f"Film '{name}' erfolgreich aktualisiert!")
        else:
            print("Fehler: Film nicht gefunden!")
    except ValueError:
        print("Ungültige Bewertung. Bitte eine Zahl eingeben.")

def stats():
    """
    Zeigt Statistiken zu den Filmen an.
    Beinhaltet:
    - Durchschnittsbewertung
    - Median bewertung
    - Beste(r) Film(e)
    - Schlechteste(r) Film(e)
    gibt eine Meldung aus, wenn keine Filme in der Datenbank sind.
    """
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    ratings = list(movies.values())
    average = sum(ratings) / len(ratings)
    median = statistics.median(ratings)
    best_rating = max(ratings)
    worst_rating = min(ratings)
    best_movies = [name for name, rating in movies.items() if rating == best_rating]
    worst_movies = [name for name, rating in movies.items() if rating == worst_rating]

    print(f"Durchschnittliche Bewertung: {average:.1f}")
    print(f"Median der Bewertungen: {median}")
    print("Bester Film(e):", ", ".join(best_movies))
    print("Schlechtester Film(e):", ", ".join(worst_movies))

def random_movie():
    """
    Gibt einen zufällig ausgewählten Film und dessen Bewertung aus.
    Gibt eine Meldung aus, wenn keine Filme in der Datenbank sind.
    """
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    name, rating = random.choice(list(movies.items()))
    print(f"Zufälliger Film: {name}, {rating}")

def search_movie():
    """
    Durchsucht Filme nach einem Teil des Namens (Groß-/Kleinschreibung wird ignoriert).
    Gibt alle Treffer mit ihren Bewertungen aus oder eine Meldung, wenn keine Filme gefunden werden.
    """
    try:
        query = input("Gib einen Teil des Filmtitels ein: ").lower()
        matches = {name: rating for name, rating in movies.items() if query in name.lower()}
        if matches:
            for name, rating in matches.items():
                print(f"{name}, {rating}")
        else:
            print("Keine Filme gefunden.")
    except EOFError:
        print("Eingabefehler: Keine Eingabe verfügbar.")

def movies_sorted_by_rating():
    """
    Zeigt alle Filme sortiert nach ihren Bewertungen in absteigender Reihenfolge.
    Gibt eine Meldung aus, wenn keine Filme in der Datenbank sind.
    """
    if not movies:
        print("Keine Filme in der Datenbank.")
        return

    sorted_movies = sorted(movies.items(), key=lambda item: item[1], reverse=True)
    for name, rating in sorted_movies:
        print(f"{name}: {rating}")

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