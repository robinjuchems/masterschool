import sys

def load_data():
    """
    Load sample data representing ships and their countries.
    This function serves as a placeholder for a real database or API call.
    """
    return {
        "ships": [
            {"name": "Titanic", "country": "United Kingdom"},
            {"name": "Olympic", "country": "United Kingdom"},
            {"name": "Lusitania", "country": "United States"},
            {"name": "Aquitania", "country": "United Kingdom"},
            {"name": "Bismarck", "country": "Germany"}
        ]
    }

# functions
def help_command():
    """
    Display the list of available commands and their descriptions.
    Provides guidance on how to use the application.
    """
    print("""
Available commands:
  help                - Displays this help message with available commands.
  show_countries      - Shows a list of unique ship countries in alphabetical order.
  show_all_countries  - Shows all countries of the ships, including duplicates.
  show_names          - Displays the names of all ships.
  count_ships         - Displays the total number of ships.
  top_countries <n>   - Displays the top <n> countries with the most ships.
    """)

def count_ships(all_data):
    """
    Print the total number of ships in the dataset.
    """
    print(f"Total number of ships: {len(all_data['ships'])}")

def show_all_countries(all_data):
    """
    Print all the countries of the ships, including duplicates.
    """
    print("Countries of all ships (including duplicates):")
    for ship in all_data['ships']:
        print(f"- {ship['country']}")

def show_countries(all_data):
    """
    Display a list of unique ship countries sorted alphabetically.
    Uses a set to eliminate duplicate countries.
    """
    unique_countries = sorted(set(ship['country'] for ship in all_data['ships']))
    print("Countries of ships:")
    for country in unique_countries:
        print(f"- {country}")

def show_ship_names(all_data):
    """
    Display the names of all ships in the dataset.
    Iterates through the list of ships and prints each name.
    """
    print("Ship names:")
    for ship in all_data['ships']:
        print(f"- {ship['name']}")

def top_countries(all_data, num_countries):
    """
    Display the top `num_countries` with the highest number of ships.
    Counts ships by country and sorts them in descending order.
    Args:
        all_data (dict): Dataset containing ship information.
        num_countries (int): Number of top countries to display.
    """
    # Count ships per country
    country_counts = {}
    for ship in all_data['ships']:
        country = ship['country']
        country_counts[country] = country_counts.get(country, 0) + 1

    # Sort countries by ship count (descending)
    sorted_counts = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"Top {num_countries} countries with the most ships:")
    for country, count in sorted_counts[:num_countries]:
        print(f"- {country}: {count}")

def main():
    """
    Main function to handle command-line interface logic.
    Reads commands from the user and performs corresponding actions.
    """
    # Load data from external file
    all_data = load_data()

    # Check if a command is provided
    if len(sys.argv) < 2:
        print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
        return

    # Extract and process the command
    command = sys.argv[1].lower()

    # Handle commands
    if command == "help":
        help_command()
    elif command == "show_countries":
        show_countries(all_data)
    elif command == "show_all_countries":
        show_all_countries(all_data)
    elif command == "show_names":
        show_ship_names(all_data)
    elif command == "count_ships":
        count_ships(all_data)
    elif command == "top_countries":
        # Ensure a valid number argument is provided
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Error: Please provide a valid number. Example: top_countries 3")
        else:
            top_countries(all_data, int(sys.argv[2]))
    else:
        # Handle unknown commands
        print(f"Error: Unknown command '{command}'. Enter 'help' to view available commands.")

# Main entry point
if __name__ == "__main__":
    main()