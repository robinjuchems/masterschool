from jinja2 import Template
import json
import os

# HTML-Template als mehrzeiliger String
TEMPLATE_HTML = """
<html>
<head>
  <meta charset="UTF-8">
  <title>Animal Repository</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #ffe9e9; padding: 20px; }
    h1 { text-align: center; }
    .cards { list-style: none; padding: 0; }
    .cards__item { background-color: white; border-radius: 0.25rem; padding: 1rem; margin: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .card__title { font-size: 1.25rem; font-weight: bold; }
    .card__text { font-size: 1rem; }
  </style>
</head>
<body>
  <h1>Animal Repository</h1>
  <ul class="cards">
    {% if animals %}
      {% for animal in animals %}
        <li class="cards__item">
          <div class="card__title">{{ animal.name }}</div>
          <div class="card__text">
            {% if animal.characteristics and animal.characteristics.slogan %}
              {{ animal.characteristics.slogan }}
            {% elif animal.taxonomy and animal.taxonomy.scientific_name %}
              Scientific Name: {{ animal.taxonomy.scientific_name }}
            {% else %}
              No additional information available.
            {% endif %}
          </div>
        </li>
      {% endfor %}
    {% else %}
      <li>No animals found for "{{ animal_name }}".</li>
    {% endif %}
  </ul>
</body>
</html>
"""

def load_data(file_path: str) -> list:
    """Lädt eine JSON-Datei und gibt ihren Inhalt zurück."""
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden. Bitte stelle sicher, dass 'animals_data.json' existiert.")
        return []
    except json.JSONDecodeError:
        print(f"Fehler: '{file_path}' enthält ungültiges JSON. Überprüfe das Dateiformat.")
        return []
    except Exception as e:
        print(f"Unerwarteter Fehler beim Laden der Datei '{file_path}': {e}")
        return []

def fetch_local_data(animal_name: str) -> list:
    """Filtert Tiere aus der JSON-Datei basierend auf dem eingegebenen Namen."""
    all_animals = load_data('animals_data.json')
    if not all_animals:
        return []
    # Filtere Tiere, deren Name den eingegebenen String enthält (case-insensitive)
    filtered_animals = [animal for animal in all_animals if animal_name.lower() in animal.get('name', '').lower()]
    return filtered_animals

def generate_website(animal_name: str, animals: list) -> None:
    """Generiert die HTML-Website und schreibt sie in eine Datei oder gibt sie in der Konsole aus."""
    template = Template(TEMPLATE_HTML)
    rendered_html = template.render(animal_name=animal_name, animals=animals)
    
    # Verwende ein schreibbares Verzeichnis in Codio
    output_file = '/home/codio/workspace/animals.html'
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        print(f"Die Website wurde erfolgreich in '{output_file}' generiert.")
        print(f"Öffne '{output_file}' im Browser, um das Ergebnis zu sehen!")
    except OSError as e:
        print(f"Fehler: Konnte '{output_file}' nicht schreiben (möglicherweise schreibgeschützt): {e}")
        print("Der generierte HTML-Inhalt wird stattdessen in der Konsole angezeigt:")
        print("-" * 50)
        print(rendered_html)
        print("-" * 50)
    except Exception as e:
        print(f"Unerwarteter Fehler beim Schreiben der Datei: {e}")

def main() -> None:
    """Hauptfunktion: Fragt nach einem Tiernamen und generiert die Website in einer Schleife."""
    print("Willkommen im Animal Repository!")
    print("Gib einen Tiernamen ein, um Informationen anzuzeigen, oder 'quit' zum Beenden.")
    
    while True:
        animal_name = input("Bitte gib einen Tiernamen ein: ").strip()
        
        # Beende das Programm, wenn der Benutzer 'quit' eingibt
        if animal_name.lower() == 'quit':
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        
        # Überprüfe, ob die Eingabe leer ist
        if not animal_name:
            print("Der Tiername darf nicht leer sein. Versuche es erneut.")
            continue
        
        # Hole die gefilterten Daten
        animals = fetch_local_data(animal_name)
        
        # Generiere die Website
        if not animals:
            print(f"Keine Tiere für '{animal_name}' gefunden. Versuche einen anderen Namen.")
        else:
            print(f"{len(animals)} Tier(e) für '{animal_name}' gefunden.")
            generate_website(animal_name, animals)

if __name__ == "__main__":
    main()
