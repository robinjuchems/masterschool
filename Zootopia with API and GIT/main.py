import json


def load_data(file_path: str) -> list:
    """Lädt eine JSON-Datei und gibt ihren Inhalt zurück."""
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
        return []
    except json.JSONDecodeError:
        print(f"Fehler beim Decodieren der JSON-Datei '{file_path}'.")
        return []


def serialize_animal(animal_obj: dict) -> str:
    """Serialisiert ein Tierobjekt in eine HTML-Karte."""
    output = '<li class="cards__item">\n'

    # Name als Titel
    name = animal_obj.get('name', 'Unbekannt')
    output += f'    <div class="card__title">{name}</div>\n'

    # Andere Felder im Textbereich
    output += '    <p class="card__text">\n'
    characteristics = animal_obj.get('characteristics', {})

    diet = characteristics.get('diet')
    if diet:
        output += f'        <strong>Diet:</strong> {diet}<br/>\n'

    locations = animal_obj.get('locations', [])
    if locations:
        output += f'        <strong>Location:</strong> {locations[0]}<br/>\n'

    animal_type = characteristics.get('type')
    if animal_type:
        output += f'        <strong>Type:</strong> {animal_type}<br/>\n'

    output += '    </p>\n'
    output += '</li>\n'
    return output


def generate_animal_string(animals_data: list) -> str:
    """Generiert einen String mit HTML-Karten für alle Tiere."""
    if not animals_data:
        return '<li class="cards__item">Keine Tiere gefunden.</li>\n'
    return ''.join(serialize_animal(animal) for animal in animals_data)


def generate_html() -> None:
    """Liest das Template, ersetzt den Platzhalter und schreibt in animals.html."""
    # Lade die Tierdaten
    animals_data = load_data('animals_data.jason')

    # Lade das HTML-Template
    try:
        with open('animals_template.html', 'r', encoding="utf-8") as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print("Die Template-Datei 'animals_template.html' wurde nicht gefunden.")
        return

    # Ersetze den Platzhalter mit den Tierdaten
    animal_data = generate_animal_string(animals_data)
    html_content = template_content.replace('__REPLACE_ANIMALS_INFO__', animal_data)

    # Schreibe die generierte HTML-Datei
    try:
        with open('animals.html', 'w', encoding="utf-8") as output_file:
            output_file.write(html_content)
        print("HTML-Seite erfolgreich als 'animals.html' generiert!")
    except Exception as e:
        print(f"Fehler beim Schreiben der HTML-Datei: {e}")


if __name__ == "__main__":
    generate_html()