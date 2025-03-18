import movie_storage

def list_movies():
    """Zeigt alle Filme in der Datenbank an."""
    movies = movie_storage.get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return
    print(f"{len(movies)} Filme insgesamt:")
    for title, details in movies.items():
        print(f"{title} ({details['year']}): {details['rating']}")

def add_movie():
    """Fügt einen neuen Film hinzu."""
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
    if movie_storage.add_movie(title, year, rating):
        print(f"Film '{title}' erfolgreich hinzugefügt!")
    else:
        print(f"Der Film '{title}' existiert bereits in der Datenbank.")

def delete_movie():
    """Löscht einen Film aus der Datenbank."""
    title = input("Titel des zu löschenden Films: ")
    if movie_storage.delete_movie(title):
        print(f"Film '{title}' erfolgreich gelöscht!")
    else:
        print(f"Fehler: Film '{title}' nicht gefunden.")

def update_movie():
    """Aktualisiert die Bewertung eines Films."""
    title = input("Titel des zu aktualisierenden Films: ")
    try:
        new_rating = float(input("Neue Bewertung (0-10): "))
        if not (0 <= new_rating <= 10):
            print("Fehler: Die Bewertung muss zwischen 0 und 10 liegen.")
            return
    except ValueError:
        print("Fehler: Ungültige Bewertung.")
        return
    if movie_storage.update_movie(title, new_rating):
        print(f"Film '{title}' erfolgreich aktualisiert!")
    else:
        print(f"Fehler: Film '{title}' nicht gefunden.")

def stats():
    """Zeigt Statistiken zu den Filmen an."""
    stats_data = movie_storage.get_stats()
    if stats_data is None:
        print("Keine Filme in der Datenbank.")
        return
    print(f"Durchschnittliche Bewertung: {stats_data['average']:.1f}")
    print(f"Median der Bewertungen: {stats_data['median']}")
    print("Bester Film(e):", ", ".join(stats_data['best_movies']))
    print("Schlechtester Film(e):", ", ".join(stats_data['worst_movies']))

def search_movie():
    """Sucht nach Filmen anhand eines Suchbegriffs."""
    query = input("Suchbegriff: ")
    matches = movie_storage.search_movie(query)
    if matches:
        for title, details in matches.items():
            print(f"{title} ({details['year']}): {details['rating']}")
    else:
        print("Keine Filme gefunden.")

def movies_sorted_by_rating():
    """Zeigt Filme sortiert nach Bewertung an."""
    sorted_movies = movie_storage.get_sorted_movies()
    if not sorted_movies:
        print("Keine Filme in der Datenbank.")
        return
    for title, details in sorted_movies:
        print(f"{title} ({details['year']}): {details['rating']}")

def random_movie():
    """Zeigt einen zufälligen Film an."""
    movie = movie_storage.get_random_movie()
    if movie is None:
        print("Keine Filme in der Datenbank.")
        return
    title, details = movie
    print(f"Zufälliger Film: {title} ({details['year']}): {details['rating']}")

def main():
    """Hauptfunktion mit Menü zur Interaktion mit der Datenbank."""
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