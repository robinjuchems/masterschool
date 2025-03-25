from jinja2 import Template
import os

# Harteingebettete Tierdaten
ANIMAL_DATA = [
    {"name": "Lion", "characteristics": {"slogan": "King of the Jungle"},
     "taxonomy": {"scientific_name": "Panthera leo"}},
    {"name": "Elephant", "characteristics": {"slogan": "Gentle Giant"},
     "taxonomy": {"scientific_name": "Loxodonta africana"}},
    {"name": "Tiger", "characteristics": {"slogan": "Fierce Hunter"},
     "taxonomy": {"scientific_name": "Panthera tigris"}},
    {"name": "Dolphin", "characteristics": {"slogan": "Playful Swimmer"},
     "taxonomy": {"scientific_name": "Delphinus delphis"}},
    {"name": "Bear", "taxonomy": {"scientific_name": "Ursus arctos"}}
]


def fetch_local_data(animal_name: str) -> list:
    """
    Filtert Tiere aus der eingebetteten Datenliste basierend auf dem eingegebenen Namen.

    Args:
        animal_name (str): Der gesuchte Tiername.
    Returns:
        list: Liste der passenden Tiere.
    """
    if not animal_name:
        return []
    return [animal for animal in ANIMAL_DATA if animal_name.lower() in animal.get('name', '').lower()]


def generate_website(animal_name: str, animals: list) -> None:
    """
    Generiert die HTML-Website mit dem Template und speichert sie oder gibt sie aus.

    Args:
        animal_name (str): Der eingegebene Tiername.
        animals (list): Liste der gefundenen Tiere.
    """
    template_path = 'animals_template.html'
    if not os.path.exists(template_path):
        print(f"Fehler: '{template_path}' wurde nicht gefunden. Bitte stelle sicher, dass die Datei existiert.")
        return

    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template_content = template_file.read()
    except Exception as e:
        print(f"Fehler beim Lesen von '{template_path}': {e}")
        return

    template = Template(template_content)
    rendered_html = template.render(animal_name=animal_name, animals=animals)

    output_file = '/home/codio/workspace/animals.html'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"\nErfolg: Die Website wurde in '{output_file}' gespeichert.")
        print("Öffne die Datei in Codio (links im Dateibaum) oder im Browser, um das Ergebnis zu sehen!")
    except OSError as e:
        print(f"\nFehler: Konnte '{output_file}' nicht schreiben (möglicherweise schreibgeschützt): {e}")
        print("Stattdessen wird der HTML-Inhalt hier angezeigt:")
        print("-" * 60)
        print(rendered_html)
        print("-" * 60)
    except Exception as e:
        print(f"\nUnerwarteter Fehler beim Speichern der Datei: {e}")


def main() -> None:
    """
    Hauptfunktion: Fragt den Benutzer nach Tiernamen und generiert die Website in einer Schleife.
    """
    print("=== Willkommen im Animal Repository ===")
    print("Dieses Programm zeigt Informationen zu Tieren an.")
    print("Gib einen Tiernamen ein (z. B. 'Lion', 'Tiger') oder 'quit' zum Beenden.")

    while True:
        animal_name = input("\nTiername: ").strip()

        # Programm beenden
        if animal_name.lower() == 'quit':
            print("Danke, dass du das Animal Repository genutzt hast. Auf Wiedersehen!")
            break

        # Eingabevalidierung
        if not animal_name:
            print("Fehler: Der Tiername darf nicht leer sein. Bitte versuche es erneut.")
            continue
        if not any(c.isalpha() for c in animal_name):
            print("Fehler: Der Tiername sollte Buchstaben enthalten. Bitte versuche es erneut.")
            continue

        # Daten abrufen und Website generieren
        animals = fetch_local_data(animal_name)
        if not animals:
            print(f"Keine Tiere für '{animal_name}' gefunden. Versuche einen anderen Namen (z. B. 'Lion', 'Elephant').")
        else:
            print(f"{len(animals)} Tier(e) für '{animal_name}' gefunden.")
            generate_website(animal_name, animals)


if __name__ == "__main__":
    main()