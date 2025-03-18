import logging

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein_geheimer_schlüssel'  # Ersetze dies mit einem sicheren Schlüssel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Logging konfigurieren
logging.basicConfig(filename='app.log', level=logging.ERROR)

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Filmmodell
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Benutzer-Loader für Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login-Formular
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Funktion zum Abrufen von Filmdaten von der OMDb API
def fetch_movie_data(title):
    try:
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return {
                "name": data["Title"],
                "director": data["Director"],
                "year": int(data["Year"]) if data["Year"].isdigit() else None,
                "rating": float(data["imdbRating"]) if "imdbRating" in data else None
            }, None
        else:
            return None, data.get("Error", "Film nicht gefunden")
    except requests.RequestException as e:
        return None, f"API-Fehler: {str(e)}"

# Routen
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form, error="Ungültiger Benutzername oder Passwort"), 401
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        if User.query.filter_by(name=name).first():
            return render_template('add_user.html', error="Benutzername bereits vergeben"), 400
        new_user = User()
        new_user.set_password("password")  # Standardpasswort
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user_movies', user_id=new_user.id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Hinzufügen des Benutzers: {str(e)}")
            return render_template('500.html', error="Fehler beim Hinzufügen des Benutzers"), 500
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = User.query.get_or_404(user_id)
    movies = Movie.query.filter_by(user_id=user_id).all()
    return render_template('movies.html', user=user, movies=movies, user_id=user_id)

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        movie_data, error = fetch_movie_data(title)
        if error:
            return render_template('add_movie.html', user_id=user_id, error=error), 400
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
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Hinzufügen des Films: {str(e)}")
            return render_template('500.html', error="Fehler beim Hinzufügen des Films"), 500
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.user_id != user_id:
        return render_template('403.html'), 403
    if request.method == 'POST':
        try:
            year = int(request.form['year']) if request.form['year'] else None
            rating = float(request.form['rating']) if request.form['rating'] else None
            if year and (year < 1888 or year > 2100):
                return render_template('update_movie.html', movie=movie, user_id=user_id, error="Ungültiges Jahr"), 400
            if rating and (rating < 0 or rating > 10):
                return render_template('update_movie.html', movie=movie, user_id=user_id, error="Ungültige Bewertung"), 400
            movie.year = year
            movie.rating = rating
            db.session.commit()
            return redirect(url_for('user_movies', user_id=user_id))
        except ValueError:
            return render_template('update_movie.html', movie=movie, user_id=user_id, error="Ungültige Eingabe"), 400
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Aktualisieren des Films: {str(e)}")
            return render_template('500.html', error="Fehler beim Aktualisieren des Films"), 500
    return render_template('update_movie.html', movie=movie, user_id=user_id)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
@login_required
def delete_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.user_id != user_id:
        return render_template('403.html'), 403
    try:
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        db.session.rollback()
        logging.error(f"Fehler beim Löschen des Films: {str(e)}")
        return render_template('500.html', error="Fehler beim Löschen des Films"), 500

# Datenbank erstellen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)