import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schlüssel'  # Für Flash-Nachrichten

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  director TEXT NOT NULL,
                  year INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Startseite: Liste aller Filme
@app.route('/')
def home():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    movies = c.fetchall()
    conn.close()
    return render_template('index.html', movies=movies, edit_movie=None)

# Film hinzufügen
@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form['title']
    director = request.form['director']
    year = request.form['year']
    if not title or not director or not year:
        flash('Alle Felder sind erforderlich!')
        return redirect(url_for('home'))
    try:
        year = int(year)
    except ValueError:
        flash('Das Jahr muss eine Ganzzahl sein!')
        return redirect(url_for('home'))
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('INSERT INTO movies (title, director, year) VALUES (?, ?, ?)', (title, director, year))
    conn.commit()
    conn.close()
    flash('Film erfolgreich hinzugefügt!')
    return redirect(url_for('home'))

# Film bearbeiten - Formular anzeigen
@app.route('/edit/<int:movie_id>', methods=['GET'])
def edit_movie_form(movie_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    movie = c.fetchone()
    conn.close()
    if movie:
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute('SELECT * FROM movies')
        movies = c.fetchall()
        conn.close()
        return render_template('index.html', movies=movies, edit_movie=movie)
    else:
        flash('Film nicht gefunden!')
        return redirect(url_for('home'))

# Film bearbeiten - Änderungen speichern
@app.route('/update/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    title = request.form['title']
    director = request.form['director']
    year = request.form['year']
    if not title or not director or not year:
        flash('Alle Felder sind erforderlich!')
        return redirect(url_for('edit_movie_form', movie_id=movie_id))
    try:
        year = int(year)
    except ValueError:
        flash('Das Jahr muss eine Ganzzahl sein!')
        return redirect(url_for('edit_movie_form', movie_id=movie_id))
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('UPDATE movies SET title = ?, director = ?, year = ? WHERE id = ?', (title, director, year, movie_id))
    conn.commit()
    conn.close()
    flash('Film erfolgreich aktualisiert!')
    return redirect(url_for('home'))

# Film löschen
@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    flash('Film erfolgreich gelöscht!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)