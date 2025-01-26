import argparse
from load_data import load_data

def calculate_column_widths(rows, headers, max_width):
    all_rows = [headers] + rows
    return [
        min(max(len(str(row[col_index])) for row in all_rows), max_width)
        for col_index in range(len(headers))
    ]

def truncate(text, width):
    return text if len(text) <= width else text[:width - 3] + "..."

def format_table(rows, headers, max_width=20):
    """
    Formatiert eine Tabelle für die Anzeige mit Text.
    """

    column_widths = calculate_column_widths(rows, headers, max_width)
    header_row = " | ".join(
        truncate(str(headers[col_index]), column_widths[col_index]).ljust(column_widths[col_index]) for col_index in
        range(len(headers)))
    separator = "-+-".join("-" * column_widths[col_index] for col_index in range(len(headers)))
    data_rows = "\n".join(
        " | ".join(
            truncate(str(row[col_index]), column_widths[col_index]).ljust(column_widths[col_index]) for col_index in
            range(len(headers)))
        for row in rows
    )
    return f"{header_row}\n{separator}\n{data_rows}"

# Command Functions
def print_welcome_message():
    """
    Gibt eine Willkommensnachricht aus.
    """
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")


def help_command():
    """
    Zeigt die verfügbaren Befehle an.
    """
    print(
        """
Available commands:
  help                - Displays this help message.
  show_countries      - Shows a list of unique ship countries in alphabetical order.
  top_countries <n>   - Displays the top <n> countries with the most ships.
  exit                - Exits the CLI.
        """
    )

def count_by_country(data):
    """
    Zählt die Schiffe nach Ländern und gibt ein Dictionary zurück.
    """
    country_counts = {}
    for ship in data.get("ships", []):
        country = ship["country"]
        country_counts[country] = country_counts.get(country, 0) + 1
    return country_counts

def show_countries(data):
    """
    Zeigt eine Liste der einzigartigen Länder sortiert nach Alphabet.
    """
    if not data.get("data"):
        print("Keine Daten verfügbar.")
        return
    unique_countries = sorted(set(ship["country"] for ship in data))
    print("Countries of ships:")
    for country in unique_countries:
        print(f"- {country}")


def top_countries(data, num_countries):
    """
    Zeigt die Top-Länder mit den meisten Schiffen an.
    """
    country_counts = count_by_country(data)
    if not country_counts:
        print("Keine Daten verfügbar.")
        return

    sorted_counts = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    table = format_table(sorted_counts[:num_countries], headers=("Country", "Ships"))
    print(f"Top {num_countries} countries with the most ships:")
    print(table)


# Main Function
def main():
    """
    Hauptfunktion zur Steuerung der Benutzerinteraktion.
    """
    parser = argparse.ArgumentParser(description="Ships CLI Tool")
    parser.add_argument("--file", type=str, default="ships_data.json", help="Pfad zur JSON-Datei mit den Schiffs-Daten")
    args = parser.parse_args()

    data = load_data(args.file)
    print_welcome_message()

    while True:
        try:
            command = input("\nEnter a command (or 'help' to view commands): ").strip().lower()
            if command == "help":
                help_command()
            elif command == "show_countries":
                show_countries(data)
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
        except KeyboardInterrupt:
            print("\nExiting the CLI. Goodbye!")
            break


if __name__ == "__main__":
    main()
