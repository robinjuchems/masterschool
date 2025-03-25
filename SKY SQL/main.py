"""
Sky SQL - Flugdatenverwaltung

Dieses Programm bietet eine Benutzeroberfläche zur Abfrage von Flugdaten aus einer SQLite-Datenbank.
Es unterstützt alle 7 Abfragen aus der Aufgabe 'Day 2 - Data Queries'.
"""

from datetime import datetime
from data import FlightData
from typing import List

SQLITE_URI = 'sqlite:///data/flights.sqlite3'  # Korrigierter URI
IATA_LENGTH = 3


def flight_by_id(data_manager: FlightData) -> None:
    """Query 1 & 2: Zeigt Informationen zu einem Flug basierend auf seiner ID an."""
    while True:
        try:
            flight_id = int(input("Enter flight ID: ").strip())
            results = data_manager.get_flight_by_id(flight_id)
            print_results(results, f"Flugdetails für ID {flight_id}")
            break
        except ValueError:
            print("Ungültige Eingabe. Bitte eine numerische Flug-ID eingeben.")


def flights_by_date(data_manager: FlightData) -> None:
    """Query 3: Zeigt Flüge an, die an einem bestimmten Datum stattfinden."""
    while True:
        date_input = input("Enter date in DD/MM/YYYY format: ").strip()
        try:
            date_obj = datetime.strptime(date_input, '%d/%m/%Y')
            results = data_manager.get_flights_by_date(date_obj.day, date_obj.month, date_obj.year)
            print_results(results, f"Flüge am {date_input}")
            break
        except ValueError as error:
            print(f"Ungültiges Datumsformat. Bitte DD/MM/YYYY verwenden. Fehler: {error}")


def delayed_flights_by_airline(data_manager: FlightData) -> None:
    """Unterstützt Query 5: Zeigt verspätete Flüge einer bestimmten Fluggesellschaft an."""
    airline_input = input("Enter airline name: ").strip()
    if not airline_input:
        print("Bitte einen Namen eingeben.")
        return
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results, f"Verspätete Flüge für Fluggesellschaft '{airline_input}'")


def delayed_flights_by_airport(data_manager: FlightData) -> None:
    """Query 6: Zeigt verspätete Flüge von einem bestimmten Abflugflughafen an."""
    while True:
        airport_input = input("Enter origin airport IATA code: ").upper().strip()
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            results = data_manager.get_delayed_flights_by_airport(airport_input)
            print_results(results, f"Verspätete Flüge von Flughafen {airport_input}")
            break
        print("Ungültiger IATA-Code (muss 3 Buchstaben sein). Versuche es erneut.")


def additional_queries(data_manager: FlightData) -> None:
    """Führt Query 4, 5 und 7 aus."""
    # Query 4: Alle verspäteten Flüge
    print("\nQuery 4 - Alle verspäteten Flüge (sortiert nach Verspätung):")
    results = data_manager.get_all_delayed_flights()
    print_results(results, "Alle verspäteten Flüge")

    # Query 5: Durchschnittliche Verspätung pro Fluggesellschaft
    print("\nQuery 5 - Durchschnittliche Verspätung pro Fluggesellschaft:")
    results = data_manager.get_average_delay_by_airline()
    print_results(results, "Durchschnittliche Verspätung pro Fluggesellschaft")

    # Query 7: Verspätete Flüge pro Tag
    print("\nQuery 7 - Anzahl verspäteter Flüge pro Tag:")
    results = data_manager.get_delayed_flights_per_day()
    print_results(results, "Verspätete Flüge pro Tag")


def print_results(results: List, title: str = "Ergebnisse") -> None:
    """Gibt die Ergebnisse einer Datenbankabfrage formatiert aus."""
    print(f"\n{title}:")
    print(f"Got {len(results)} results.")
    if not results:
        print("Keine Ergebnisse gefunden.")
        return

    for result in results:
        try:
            if 'ID' in result._mapping and 'DELAY' in result._mapping:  # Query 1-4, 6
                flight_id = result.get('ID', 'N/A')
                origin = result.get('ORIGIN_AIRPORT', 'N/A')
                destination = result.get('DESTINATION_AIRPORT', 'N/A', '')
                airline = result.get('AIRLINE', 'N/A')
                delay = int(result.get('DELAY', 0))
                flight_number = result.get('flight_number', 'N/A')
                if delay > 0:
                    print(f"{flight_id}. {origin} -> {destination} by {airline} ({flight_number}), Delay: {delay} minutes")
                else:
                    print(f"{flight_id}. {origin} -> {destination} by {airline} ({flight_number})")
            elif 'AVERAGE_DELAY' in result._mapping:  # Query 5
                airline = result.get('AIRLINE', 'N/A')
                avg_delay = round(float(result.get('AVERAGE_DELAY', 0)), 2)
                print(f"{airline}: Durchschnittliche Verspätung {avg_delay} Minuten")
            elif 'DELAYED_FLIGHTS' in result._mapping:  # Query 7
                year = result.get('year', 'N/A')
                month = result.get('month', 'N/A')
                day = result.get('day', 'N/A')
                count = result.get('DELAYED_FLIGHTS', 0)
                print(f"{day}/{month}/{year}: {count} verspätete Flüge")
            else:
                print(result)  # Fallback
        except (ValueError, TypeError) as error:
            print(f"Fehler beim Verarbeiten des Ergebnisses: {error}")


def show_menu_and_get_input() -> callable:
    """Zeigt das Menü an und gibt die ausgewählte Funktion zurück."""
    menu_options = {
        1: (flight_by_id, "Show flight by ID (Query 1 & 2)"),
        2: (flights_by_date, "Show flights by date (Query 3)"),
        3: (delayed_flights_by_airline, "Delayed flights by airline"),
        4: (delayed_flights_by_airport, "Delayed flights by origin airport (Query 6)"),
        5: (additional_queries, "Run additional queries (Query 4, 5, 7)"),
        6: (quit, "Exit")
    }
    print("\n=== Sky SQL - Flugdatenverwaltung ===")
    for key, (_, description) in menu_options.items():
        print(f"{key}. {description}")
    while True:
        try:
            choice = int(input("Choose an option (1-6): ").strip())
            if choice in menu_options:
                return menu_options[choice][0]
            print("Ungültige Option. Bitte wähle zwischen 1 und 6.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")


def main() -> None:
    """Hauptfunktion, die das Programm ausführt."""
    try:
        data_manager = FlightData(SQLITE_URI)
        print("Verbindung zur Datenbank erfolgreich hergestellt.")
        while True:
            selected_function = show_menu_and_get_input()
            selected_function(data_manager)
    except Exception as error:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {error}")
        print("Stelle sicher, dass 'data/flights.sqlite3' existiert und SQLAlchemy installiert ist.")


if __name__ == "__main__":
    main()