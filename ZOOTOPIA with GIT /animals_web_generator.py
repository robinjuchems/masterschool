import json

def load_data(file_path):
    """Loads a JSON file and returns its contents."""
    with open(file_path, "r") as handle:
        return json.load(handle)

def serialize_animal(animal_obj):
    """Serializes a single animal object into an HTML card."""
    output = '<li class="cards__item">\n'
    name = animal_obj.get('name', 'Unbekannt')
    output += f'    <div class="card__title">{name}</div>\n'
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

def generate_animal_html(animals_data):
    """Generates a string with HTML cards for all animals."""
    output = ''
    for animal in animals_data:
        output += serialize_animal(animal)
    return output

def generate_html():
    """Reads template, replaces placeholder, and writes to animals.html."""
    with open('animals_template.html', 'r') as template_file:
        template_content = template_file.read()
    animals_data = load_data('animals_data.json')
    animal_data = generate_animal_html(animals_data)
    html_content = template_content.replace('__REPLACE_ANIMALS_INFO__', animal_data)
    with open('animals.html', 'w') as output_file:
        output_file.write(html_content)
    print("HTML-Seite erfolgreich als 'animals.html' generiert!")

if __name__ == "__main__":
    generate_html()