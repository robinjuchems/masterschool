"""
Sky SQL - Flugdatenverwaltung

Dieses Programm bietet eine Benutzeroberfläche zur Abfrage von Flugdaten aus einer SQLite-Datenbank.
Es unterstützt alle 7 Abfragen aus der Aufgabe 'Day 2 - Data Queries'.
"""

from datetime import datetime
from data import FlightData
from typing import List
import os

SQLITE_URI = 'sqlite:///data/flights.sqlite3'  # Relativer Pfad, wird absolut gemacht

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
        date_input = input("Enter date in DD/MM/YYYY or DD.MM.YYYY format: ").strip()
        try:
            try:
                date_obj = datetime.strptime(date_input, '%d/%m/%Y')  # DD/MM/YYYY
            except ValueError:
                date_obj = datetime.strptime(date_input, '%d.%m.%Y')  # DD.MM.YYYY
            results = data_manager.get_flights_by_date(date_obj.day, date_obj.month, date_obj.year)
            print_results(results, f"Flüge am {date_input}")
            break
        except ValueError as error:
            print(f"Ungültiges Datumsformat. Bitte DD/MM/YYYY oder DD.MM.YYYY verwenden. Fehler: {error}")

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
        if airport_input.isalpha() and len(airport_input) == 3:
            results = data_manager.get_delayed_flights_by_airport(airport_input)
            print_results(results, f"Verspätete Flüge von Flughafen {airport_input}")
            break
        print("Ungültiger IATA-Code (muss 3 Buchstaben sein). Versuche es erneut.")

def additional_queries(data_manager: FlightData) -> None:
    """Führt Query 4, 5 und 7 aus."""
    print("\nQuery 4 - Alle verspäteten Flüge (sortiert nach Verspätung):")
    results = data_manager.get_all_delayed_flights()
    print_results(results, "Alle verspäteten Flüge")

    print("\nQuery 5 - Durchschnittliche Verspätung pro Fluggesellschaft:")
    results = data_manager.get_average_delay_by_airline()
    print_results(results, "Durchschnittliche Verspätung pro Fluggesellschaft")

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
            mapping = result._mapping

            if 'ID' in mapping and 'year' in mapping:
                flight_id = mapping.get('ID', 'N/A')
                year = mapping.get('year', 'N/A')
                month = mapping.get('month', 'N/A')
                day = mapping.get('day', 'N/A')
                origin = mapping.get('ORIGIN_AIRPORT', 'N/A')
                destination = mapping.get('DESTINATION_AIRPORT', 'N/A')
                airline = mapping.get('AIRLINE', 'N/A')
                delay = int(mapping.get('DELAY', 0))
                print(f"{flight_id}. {origin} -> {destination} by {airline}, Date: {day}/{month}/{year}, Delay: {delay} minutes")

            elif 'flight_number' in mapping:
                flight_id = mapping.get('ID', 'N/A')
                flight_number = mapping.get('flight_number', 'N/A')
                origin = mapping.get('ORIGIN_AIRPORT', 'N/A')
                delay = int(mapping.get('DELAY', 0))
                print(f"{flight_id}. {origin} ({flight_number}), Delay: {delay} minutes")

            elif 'AVERAGE_DELAY' in mapping:
                airline = mapping.get('AIRLINE', 'N/A')
                avg_delay = round(float(mapping.get('AVERAGE_DELAY', 0)), 2)
                print(f"{airline}: Durchschnittliche Verspätung {avg_delay} Minuten")

            elif 'DELAYED_FLIGHTS' in mapping:
                year = mapping.get('year', 'N/A')
                month = mapping.get('month', 'N/A')
                day = mapping.get('day', 'N/A')
                count = mapping.get('DELAYED_FLIGHTS', 0)
                print(f"{day}/{month}/{year}: {count} verspätete Flüge")

            else:
                print(f"Unbekanntes Ergebnisformat: {result}")
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Ergebnisses: {e}")
            print(f"Rohdaten: {result}")

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'flights.sqlite3')
    absolute_uri = f'sqlite:///{db_path}'

    try:
        data_manager = FlightData(absolute_uri)
        print("Verbindung zur Datenbank erfolgreich hergestellt.")
        while True:
            selected_function = show_menu_and_get_input()
            selected_function(data_manager)
    except ValueError as ve:
        print(f"Fehler bei der Datenbankinitialisierung: {ve}")
    except Exception as error:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {error}")

if __name__ == "__main__":
    main()