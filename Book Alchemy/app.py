"""
Book Alchemy - Eine Webanwendung zur Verwaltung von Büchern und Autoren.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from data_models import db, Author, Book

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE_PATH = os.path.join(DATA_DIR, 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)

db.init_app(app)

print(f"Database path: {DATABASE_PATH}")

@app.route('/')
def index():
    search_term = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'title')

    query = Book.query.join(Author)
    if search_term:
        query = query.filter(
            (Book.title.ilike(f'%{search_term}%')) |
            (Author.name.ilike(f'%{search_term}%')) |
            (Book.isbn.ilike(f'%{search_term}%'))
        )

    if sort_by == 'title':
        books = query.order_by(Book.title).all()
    elif sort_by == 'author':
        books = query.order_by(Author.name).all()
    elif sort_by == 'year':
        books = query.order_by(Book.publication_year).all()
    else:
        books = query.all()

    authors = Author.query.all()
    return render_template('home.html', books=books, authors=authors, search_term=search_term, sort_by=sort_by)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title', '').strip()
    author_name = request.form.get('author', '').strip()
    isbn = request.form.get('isbn', '').strip()
    publication_year = request.form.get('publication_year', '').strip()

    if not all([title, author_name, isbn, publication_year]):
        flash("Titel, Autor, ISBN und Veröffentlichungsjahr sind erforderlich.", "error")
        return redirect(url_for('index'))

    try:
        publication_year = int(publication_year)
    except ValueError:
        flash("Veröffentlichungsjahr muss eine Zahl sein.", "error")
        return redirect(url_for('index'))

    existing_author = Author.query.filter_by(name=author_name).first()
    if not existing_author:
        existing_author = Author(name=author_name)
        db.session.add(existing_author)

    new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author=existing_author)
    try:
        db.session.add(new_book)
        db.session.commit()
        flash(f"Buch '{title}' hinzugefügt.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Fehler beim Hinzufügen: ISBN bereits vorhanden oder andere Integritätsverletzung.", "error")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Fehler beim Hinzufügen: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    try:
        db.session.delete(book)
        db.session.commit()
        flash(f"Buch '{book.title}' gelöscht.", "success")
        if not author.books:
            db.session.delete(author)
            db.session.commit()
            flash(f"Autor '{author.name}' wurde ebenfalls gelöscht, da keine Bücher mehr existieren.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen: {str(e)}", "error")

    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        try:
            db.engine.connect()
            print("Datenbankverbindung erfolgreich.")
        except Exception as e:
            print(f"Datenbankverbindung fehlgeschlagen: {e}")
            exit(1)
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002)