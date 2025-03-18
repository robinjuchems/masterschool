"""
Book Alchemy - Eine Webanwendung zur Verwaltung von Büchern und Autoren.

Diese Anwendung verwendet Flask und SQLAlchemy, um eine SQLite-Datenbank zu verwalten,
Bücher und Autoren anzuzeigen und Bücher zu löschen, wobei Autoren ohne Bücher ebenfalls
entfernt werden. Alle Datenbankmodelle sind in dieser Datei enthalten.
"""

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug import Response

# Flask-Anwendung initialisieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dein_geheimer_schluessel'  # Für Flash-Nachrichten erforderlich

# SQLAlchemy initialisieren
db = SQLAlchemy(app)


class Author(db.Model):
    """
    Modell für einen Autor in der Datenbank.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        """Gibt eine String-Repräsentation des Autors zurück."""
        return f"Author(name='{self.name}')"


class Book(db.Model):
    """
    Modell für ein Buch in der Datenbank.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    def __repr__(self) -> str:
        """Gibt eine String-Repräsentation des Buches zurück."""
        return f"Book(title='{self.title}')"


@app.route('/')
def index() -> str:
    """Zeigt die Homepage mit einer Liste aller Bücher und Autoren an."""
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('home.html', books=books, authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id: int) -> Response:
    """
    Löscht ein Buch anhand seiner ID und den zugehörigen Autor, falls keine Bücher übrig sind.

    Parameter:
        book_id (int): Die ID des zu löschenden Buches.
    """
    lovebook = Book.query.get_or_404(book_id)
    love = lovebook.author  # Speichere den Autor vor dem Löschen

    try:
        db.session.delete(lovebook)
        db.session.commit()
        flash(f"Book '{lovebook.title}' has been successfully deleted.", "success")
    except Exception as error:
        db.session.rollback()
        flash(f"Error deleting book: {error}", "error")
        return redirect(url_for('index'))

    if not love.books:  # Lösche den Autor, wenn keine Bücher mehr vorhanden sind
        try:
            db.session.delete(love)
            db.session.commit()
            flash(f"Author '{love.name}' was deleted because no books remain.", "info")
        except Exception as error:
            db.session.rollback()
            flash(f"Error deleting author: {error}", "error")

    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Erstellt die Tabellen, falls sie nicht existieren
        # Optional: Testdaten hinzufügen
        if not Author.query.first():  # Nur hinzufügen, wenn die Datenbank leer ist
            author = Author(name="J.K. Rowling")
            book = Book(title="Harry Potter", author=author)
            db.session.add(author)
            db.session.add(book)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5002)  # Codio erwartet Port 5002