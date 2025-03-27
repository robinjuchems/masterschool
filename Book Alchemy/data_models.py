"""
data_models.py - Datenbankmodelle für Book Alchemy
"""

from flask_sqlalchemy import SQLAlchemy

# Erstelle die SQLAlchemy-Instanz
db = SQLAlchemy()

class Author(db.Model):
    """Modell für einen Autor."""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Author(name='{self.name}')"

    def __str__(self):
        return self.name

class Book(db.Model):
    """Modell für ein Buch."""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    def __repr__(self):
        return f"Book(title='{self.title}')"

    def __str__(self):
        return self.title