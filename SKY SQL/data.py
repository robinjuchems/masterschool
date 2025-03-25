"""
Data Access Layer für Flugdaten.

Dieses Modul stellt eine FlightData-Klasse bereit, die die Verbindung zu einer SQLite-Datenbank
mit SQLAlchemy abstrahiert und Methoden zum Abfragen von Flugdaten bietet. Ein Flug gilt als
verspätet, wenn seine Verspätung nicht NULL ist und mindestens 20 Minuten beträgt.
"""

from sqlalchemy import create_engine, text
from typing import List, Dict, Any, Optional


class FlightData:
    """
    Bietet Methoden zum Abfragen von Flugdaten aus einer SQLite-Datenbank.
    """

    def __init__(self, db_uri: str) -> None:
        """
        Initialisiert eine neue FlightData-Instanz mit dem angegebenen Datenbank-URI.

        Parameter:
            db_uri (str): Der Datenbank-URI (z. B. 'sqlite:///data/flights.sqlite3')

        Raises:
            ValueError: Wenn der URI ungültig ist.
        """
        if not db_uri.startswith('sqlite:///'):
            raise ValueError("Ungültiger Datenbank-URI: Muss mit 'sqlite:///' beginnen.")
        self.engine = create_engine(db_uri)

    def _execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List:
        """
        Führt die angegebene SQL-Abfrage mit optionalen Parametern aus.

        Parameter:
            query (str): Die auszuführende SQL-Abfrage.
            params (dict, optional): Zu bindende Parameter für die Abfrage.

        Rückgabe:
            list: Eine Liste von SQLAlchemy-Row-Objekten mit den Abfrageergebnissen.

        Raises:
            Exception: Bei Datenbankfehlern (wird abgefangen und leer zurückgegeben).
        """
        try:
            with self.engine.connect() as conn:
                result_obj = conn.execute(text(query), params or {})
                return result_obj.fetchall()
        except Exception as e:
            print(f"Datenbankfehler bei Abfrage: {e}")
            return []

    def get_flight_by_id(self, flight_id: int) -> List:
        """
        Query 1 & 2: Ruft Flugdaten für eine bestimmte Flug-ID ab.

        Parameter:
            flight_id (int): Die Flug-ID.

        Rückgabe:
            list: Abfrageergebnisse als Liste von Row-Objekten.
        """
        query = (
            "SELECT id AS ID, "
            "year, month, day, "
            "origin_airport AS ORIGIN_AIRPORT, "
            "destination_airport AS DESTINATION_AIRPORT, "
            "airline AS AIRLINE, "
            "departure_delay AS DELAY "
            "FROM flights "
            "WHERE id = :flight_id"
        )
        return self._execute_query(query, {"flight_id": flight_id})

    def get_flights_by_date(self, day: int, month: int, year: int) -> List:
        """
        Query 3: Ruft Flüge für ein gegebenes Datum ab.

        Parameter:
            day (int): Tag des Monats (1-31).
            month (int): Monat (1-12).
            year (int): Jahr (z. B. 2015).

        Rückgabe:
            list: Abfrageergebnisse als Liste von Row-Objekten.
        """
        query = (
            "SELECT id AS ID, "
            "flight_number, "
            "origin_airport AS ORIGIN_AIRPORT, "
            "departure_delay AS DELAY "
            "FROM flights "
            "WHERE year = :year AND month = :month AND day = :day"
        )
        return self._execute_query(query, {"day": day, "month": month, "year": year})

    def get_delayed_flights_by_airline(self, airline_name: str) -> List:
        """
        Unterstützt Query 5 (angepasst): Ruft verspätete Flüge für eine Fluggesellschaft ab.

        Parameter:
            airline_name (str): Teil des Fluggesellschaftsnamens.

        Rückgabe:
            list: Abfrageergebnisse als Liste von Row-Objekten.
        """
        query = (
            "SELECT id AS ID, "
            "flight_number, "
            "origin_airport AS ORIGIN_AIRPORT, "
            "destination_airport AS DESTINATION_AIRPORT, "
            "airline AS AIRLINE, "
            "departure_delay AS DELAY "
            "FROM flights "
            "WHERE airline LIKE :airline_name "
            "AND departure_delay IS NOT NULL "
            "AND departure_delay >= 20"
        )
        return self._execute_query(query, {"airline_name": f"%{airline_name}%"})

    def get_delayed_flights_by_airport(self, airport_code: str) -> List:
        """
        Query 6: Ruft verspätete Flüge von einem bestimmten Abflugflughafen ab.

        Parameter:
            airport_code (str): Der IATA-Code des Abflugflughafens.

        Rückgabe:
            list: Abfrageergebnisse als Liste von Row-Objekten.
        """
        query = (
            "SELECT id AS ID, "
            "flight_number, "
            "origin_airport AS ORIGIN_AIRPORT, "
            "departure_delay AS DELAY "
            "FROM flights "
            "WHERE origin_airport = :airport_code "
            "AND departure_delay > 0"
        )
        return self._execute_query(query, {"airport_code": airport_code})

    def get_all_delayed_flights(self) -> List:
        """
        Query 4: Ruft alle verspäteten Flüge ab, sortiert nach Verspätung.

        Rückgabe:
            list: Abfrageergebnisse als Liste von Row-Objekten.
        """
        query = (
            "SELECT id AS ID, "
            "year, month, day, "
            "origin_airport AS ORIGIN_AIRPORT, "
            "destination_airport AS DESTINATION_AIRPORT, "
            "departure_delay AS DELAY "
            "FROM flights "
            "WHERE departure_delay > 0 "
            "ORDER BY departure_delay DESC"
        )
        return self._execute_query(query)

    def get_average_delay_by_airline(self) -> List:
        """
        Query 5: Berechnet die durchschnittliche Verspätung pro Fluggesellschaft.

        Rückgabe:
            list: Liste von Row-Objekten mit Fluggesellschaft und Durchschnitt.
        """
        query = (
            "SELECT airline AS AIRLINE, AVG(departure_delay) AS AVERAGE_DELAY "
            "FROM flights "
            "GROUP BY airline"
        )
        return self._execute_query(query)

    def get_delayed_flights_per_day(self) -> List:
        """
        Query 7: Zählt verspätete Flüge pro Tag.

        Rückgabe:
            list: Liste von Row-Objekten mit Datum und Anzahl.
        """
        query = (
            "SELECT year, month, day, COUNT(*) AS DELAYED_FLIGHTS "
            "FROM flights "
            "WHERE departure_delay > 0 "
            "GROUP BY year, month, day "
            "ORDER BY year, month, day"
        )
        return self._execute_query(query)


if __name__ == "__main__":
    SQLITE_URI = 'sqlite:///data/flights.sqlite3'
    try:
        data_layer = FlightData(SQLITE_URI)
        print("Test - Flug mit ID 280:", data_layer.get_flight_by_id(280))
    except Exception as e:
        print(f"Fehler beim Test: {e}")