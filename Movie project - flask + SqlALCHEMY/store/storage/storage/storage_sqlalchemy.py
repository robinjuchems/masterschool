import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from istorage import istorage
from .models import Base, Movie

class StorageSqlAlchemy(istorage):
    def __init__(self, db_path="data/movies.db"):
        """Initialisiert die StorageSqlAlchemy-Klasse mit einem Datenbankpfad."""
        # Erstelle das Verzeichnis, falls es nicht existiert
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # Erstelle die Datenbankverbindung
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        """
        session = self.Session()
        try:
            movies = session.query(Movie).all()
            return {movie.name: movie.to_dict() for movie in movies}
        finally:
            session.close()

    def add_movie(self, title, year, rating, poster=None):
        """
        Adds a movie to the movies database.
        """
        session = self.Session()
        try:
            # Prüfe, ob der Film bereits existiert
            if session.query(Movie).filter_by(name=title).first():
                print(f"Film '{title}' existiert bereits.")
                return
            movie = Movie(name=title, year=year, rating=rating, user_id=1)  # Standardmäßig user_id=1
            session.add(movie)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Hinzufügen des Films: {e}")
        finally:
            session.close()

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(name=title).first()
            if movie:
                session.delete(movie)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Löschen des Films: {e}")
        finally:
            session.close()

    def update_movie(self, title, rating):
        """
        Updates a movie in the movies database.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(name=title).first()
            if movie:
                movie.rating = rating
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Aktualisieren des Films: {e}")
        finally:
            session.close()