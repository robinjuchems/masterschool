from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    user_id = Column(Integer, nullable=False)

    def to_dict(self):
        """
        Konvertiert das Movie-Objekt in ein Dictionary.
        """
        return {
            "name": self.name,
            "director": self.director,
            "year": self.year,
            "rating": self.rating,
            "user_id": self.user_id
        }