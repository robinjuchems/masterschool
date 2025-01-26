import argparse
from load_data import load_data


def show_countries(data):
    """
    Zeigt eine Liste der einzigartigen Länder sortiert nach Alphabet.
    """
    ships = data.get("data", [])  # Zugriff auf den korrekten Schlüssel
    if not ships:
        print("Keine Daten verfügbar.")
        return

    unique_countries = sorted(set(ship.get("COUNTRY", "Unbekannt") for ship in ships))
    print("Countries of ships:")
    for country in unique_countries:
        print(f"- {country}")


def count_by_country(data):
    """
    Zählt die Schiffe nach Ländern und gibt ein Dictionary zurück.
    """
    ships = data.get("data", [])  # Zugriff auf den korrekten Schlüssel
    country_counts = {}
    for ship in ships:
        country = ship.get("COUNTRY", "Unbekannt")
        country_counts[country] = country_counts.get(country, 0) + 1
    return country_counts


def top_countries(data, num_countries):
    """
    Zeigt die Top-Länder mit den meisten Schiffen an.
    """
    country_counts = count_by_country(data)
    if not country_counts:
        print("Keine Daten verfügbar.")
        return

    sorted_counts = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"Top {num_countries} countries with the most ships:")
    for country, count in sorted_counts[:num_countries]:
        print(f"{country}: {count}")


def count_ships(data):
    """
    Gibt die Gesamtanzahl der Schiffe aus.
    """
    ships = data.get("data", [])
    print(f"Total number of ships: {len(ships)}")


def list_ship_names(data):
    """
    Gibt die Namen aller Schiffe aus.
    """
    ships = data.get("data", [])
    if not ships:
        print("Keine Daten verfügbar.")
        return
    print("Ship names:")
    for ship in ships:
        print(f"- {ship.get('SHIPNAME', 'Unknown')}")


def list_all_countries(data):
    """
    Gibt alle Länder der Schiffe aus.
    """
    ships = data.get("data", [])
    if not ships:
        print("Keine Daten verfügbar.")
        return
    print("All ship countries:")
    for ship in ships:
        print(f"- {ship.get('COUNTRY', 'Unknown')}")


def list_unique_countries(data):
    """
    Gibt alle einzigartigen Länder der Schiffe aus.
    """
    ships = data.get("data", [])
    if not ships:
        print("Keine Daten verfügbar.")
        return
    unique_countries = sorted(set(ship.get("COUNTRY", "Unknown") for ship in ships))
    print("Unique ship countries:")
    for country in unique_countries:
        print(f"- {country}")


def main():
    parser = argparse.ArgumentParser(description="Ships CLI Tool")
    parser.add_argument("--file", type=str, default="ships_data.json", help="Pfad zur JSON-Datei mit den Schiffs-Daten")
    args = parser.parse_args()

    data = load_data(args.file)
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")

    while True:
        command = input("\nEnter a command (or 'help' to view commands): ").strip().lower()
        if command == "help":
            print(
                "Available commands: count_ships, list_ship_names, list_all_countries, list_unique_countries, top_countries <n>, show_countries, exit")
        elif command == "show_countries":
            show_countries(data)
        elif command == "count_ships":
            count_ships(data)
        elif command == "list_ship_names":
            list_ship_names(data)
        elif command == "list_all_countries":
            list_all_countries(data)
        elif command == "list_unique_countries":
            list_unique_countries(data)
        elif command.startswith("top_countries"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                top_countries(data, int(parts[1]))
            else:
                print("Error: Ungültige Eingabe. Beispiel: top_countries 3")
        elif command == "exit":
            print("Exiting the CLI. Goodbye!")
            break
        else:
            print(f"Error: Unknown command '{command}'. Enter 'help' to view available commands.")


if __name__ == "__main__":
    main()