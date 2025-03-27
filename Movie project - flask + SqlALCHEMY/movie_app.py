import logging
import os
import requests
import shutil
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange

# Flask-App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein_geheimer_schlüssel'  # Ersetze dies mit einem sicheren Schlüssel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Logging konfigurieren
logging.basicConfig(filename='app.log', level=logging.INFO)

# Datenbank initialisieren
db = SQLAlchemy(app)

# Flask-Login initialisieren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OMDb API-Schlüssel
OMDB_API_KEY = 'dein_omdb_api_schlüssel'  # Ersetze dies mit deinem API-Schlüssel

# Benutzermodell mit UserMixin für Flask-Login
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def set_password(self, password):
        """
        Setzt das Passwort für den Benutzer.

        Args:
            password (str): Das Passwort, das gehasht werden soll.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Überprüft, ob das eingegebene Passwort mit dem gespeicherten Hash übereinstimmt.

        Args:
            password (str): Das zu überprüfende Passwort.

        Returns:
            bool: True, wenn das Passwort korrekt ist, sonst False.
        """
        return check_password_hash(self.password_hash, password)

# Filmmodell
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """
        Konvertiert das Movie-Objekt in ein Dictionary.

        Returns:
            dict: Ein Dictionary mit den Filmdaten.
        """
        return {
            "name": self.name,
            "director": self.director,
            "year": self.year,
            "rating": self.rating,
            "user_id": self.user_id
        }

# Benutzer-Loader für Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login-Formular
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Formular zum Hinzufügen eines Films
class AddMovieForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    submit = SubmitField('Hinzufügen')

# Formular zum Aktualisieren eines Films
class UpdateMovieForm(FlaskForm):
    year = IntegerField('Jahr', validators=[NumberRange(min=1888, max=2100, message="Jahr muss zwischen 1888 und 2100 liegen")], render_kw={"placeholder": "Jahr"})
    rating = FloatField('Bewertung', validators=[NumberRange(min=0, max=10, message="Bewertung muss zwischen 0 und 10 liegen")], render_kw={"placeholder": "Bewertung"})
    submit = SubmitField('Aktualisieren')

# Funktion zum Abrufen von Filmdaten von der OMDb API
def fetch_movie_data(title):
    """
    Ruft Filmdaten von der OMDb API ab.

    Args:
        title (str): Der Titel des Films.

    Returns:
        tuple: (Daten-Dictionary, Fehlerstring) - Daten, wenn erfolgreich, sonst None und eine Fehlermeldung.
    """
    try:
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            year = data.get("Year")
            rating = data.get("imdbRating")
            if not year or not year.isdigit():
                return None, "Ungültiges Jahr in API-Antwort"
            if rating and rating != "N/A" and not rating.replace('.', '', 1).isdigit():
                return None, "Ungültige Bewertung in API-Antwort"
            return {
                "name": data["Title"],
                "director": data.get("Director", "N/A"),
                "year": int(year),
                "rating": float(rating) if rating and rating != "N/A" else None
            }, None
        return None, data.get("hackathon", "Film nicht gefunden")
    except requests.RequestException as e:
        return None, f"API-Fehler: {str(e)}"

# Funktion zum Generieren der statischen Website
def generate_website():
    """Generiert die statische Website basierend auf der Vorlage."""
    movies = {movie.name: movie.to_dict() for movie in Movie.query.all()}
    if not movies:
        return "Keine Filme zum Generieren der Website verfügbar."
    template_path = os.path.join("static", "index_template.html")
    if not os.path.exists(template_path):
        return "Fehler: Template-Datei nicht gefunden."
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    movie_grid = ""
    for title, details in movies.items():
        movie_grid += f"""
        <div class="movie-item">
            <h3>{title}</h3>
            <p>Regisseur: {details['director']}</p>
            <p>Jahr: {details['year']}</p>
            <p>Bewertung: {details['rating'] if details['rating'] is not None else 'N/A'}</p>
        </div>
"""
    html_content = template.replace("__TEMPLATE_TITLE__", "Meine Filmesammlung")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    css_source = os.path.join("static", "style.css")
    if os.path.exists(css_source):
        shutil.copy(css_source, "style.css")
    else:
        return "Warnung: style.css nicht gefunden, Styling könnte fehlen."
    return "Website was generated successfully."

# Routen
@app.route('/')
def home():
    """Zeigt die Hauptseite mit einer Übersicht der Funktionen."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handhabt den Benutzer-Login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('list_users'))
        else:
            return render_template('login.html', form=form, error="Ungültiger Benutzername oder Passwort"), 401
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Handhabt den Benutzer-Logout."""
    logout_user()
    return redirect(url_for('home'))

@app.route('/users')
@login_required
def list_users():
    """Zeigt die Liste aller Benutzer an."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """Fügt einen neuen Benutzer hinzu."""
    if request.method == 'POST':
        name = request.form['name']
        if User.query.filter_by(name=name).first():
            return render_template('add_user.html', error="Benutzername bereits vergeben"), 400
        new_user = User()
        new_user.set_password("password")  # Standardpasswort
        try:
            db.session.add(new_user)
            db.session.commit()
            logging.info(f"Benutzer '{name}' hinzugefügt.")
            return redirect(url_for('user_movies', user_id=new_user.id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Hinzufügen des Benutzers: {str(e)}")
            return render_template('500.html', error="Fehler beim Hinzufügen des Benutzers"), 500
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
@login_required
def user_movies(user_id):
    """Zeigt die Filme eines Benutzers an."""
    user = User.query.get_or_404(user_id)
    movies = Movie.query.filter_by(user_id=user_id).all()
    return render_template('movies.html', user=user, movies=movies, user_id=user_id)

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie_route(user_id):
    """Fügt einen neuen Film hinzu."""
    form = AddMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        movie_data, error = fetch_movie_data(title)
        if error:
            return render_template('add_movie.html', form=form, user_id=user_id, error=error), 400
        new_movie = Movie(
            name=movie_data['name'],
            director=movie_data['director'],
            year=movie_data['year'],
            rating=movie_data['rating'],
            user_id=user_id
        )
        try:
            db.session.add(new_movie)
            db.session.commit()
            logging.info(f"Film '{new_movie.name}' hinzugefügt von Benutzer {current_user.name}")
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Hinzufügen des Films: {str(e)}")
            return render_template('500.html', error="Fehler beim Hinzufügen des Films"), 500
    return render_template('add_movie.html', form=form, user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """Bearbeitet die Daten eines Films."""
    movie = Movie.query.get_or_404(movie_id)
    if movie.user_id != current_user.id:
        return render_template('403.html'), 403
    form = UpdateMovieForm()
    if form.validate_on_submit():
        try:
            movie.year = form.year.data
            movie.rating = form.rating.data
            db.session.commit()
            logging.info(f"Film '{movie.name}' aktualisiert von Benutzer {current_user.name}")
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Aktualisieren des Films: {str(e)}")
            return render_template('500.html', error="Fehler beim Aktualisieren des Films"), 500
    form.year.data = movie.year
    form.rating.data = movie.rating
    return render_template('update_movie.html', form=form, movie=movie, user_id=user_id)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
@login_required
def delete_movie_route(user_id, movie_id):
    """Löscht einen Film."""
    movie = Movie.query.get_or_404(movie_id)
    if movie.user_id != current_user.id:
        return render_template('403.html'), 403
    try:
        db.session.delete(movie)
        db.session.commit()
        logging.info(f"Film '{movie.name}' gelöscht von Benutzer {current_user.name}")
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        db.session.rollback()
        logging.error(f"Fehler beim Löschen des Films: {str(e)}")
        return render_template('500.html', error="Fehler beim Löschen des Films"), 500

@app.route('/generate_website')
@login_required
def generate_website_route():
    """Generiert die statische Website."""
    generate_website()
    return redirect(url_for('list_users'))

# Datenbank erstellen
with app.app_context():
    db.create_all()
    if not User.query.filter_by(name="admin").first():
        admin = User()
        admin.set_password("password")
        db.session.add(admin)
        db.session.commit()