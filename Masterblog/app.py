from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Funktion zum Laden der Blogbeiträge
def load_blog_posts():
    """Lädt Blogbeiträge aus blog_posts.json oder gibt eine leere Liste zurück."""
    try:
        if os.path.exists('blog_posts.json'):
            with open('blog_posts.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Fehler beim Laden der Posts: {e}")
        return []

# Funktion zum Speichern der Blogbeiträge
def save_blog_posts(posts):
    """Speichert Blogbeiträge in blog_posts.json."""
    try:
        with open('blog_posts.json', 'w', encoding='utf-8') as file:
            json.dump(posts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Fehler beim Speichern der Posts: {e}")

# Funktion zum Finden eines Posts nach ID
def find_post_by_id(post_id, posts):
    """Findet einen Post anhand seiner ID oder gibt None zurück."""
    return next((p for p in posts if p['id'] == post_id), None)

# Startseite: Alle Posts anzeigen
@app.route('/')
def index():
    """Zeigt die Startseite mit allen Blogbeiträgen."""
    posts = load_blog_posts()
    return render_template('index.html', view='list', posts=posts)

# Neuer Beitrag hinzufügen
@app.route('/add', methods=['GET', 'POST'])
def add():
    """Fügt einen neuen Blogbeitrag hinzu."""
    if request.method == 'POST':
        posts = load_blog_posts()
        new_id = max([post['id'] for post in posts], default=0) + 1
        new_post = {
            'id': new_id,
            'title': request.form['title'],
            'author': request.form['author'],
            'content': request.form['content']
        }
        posts.append(new_post)
        save_blog_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='add')

# Beitrag aktualisieren
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Aktualisiert einen bestehenden Blogbeitrag."""
    posts = load_blog_posts()
    post = find_post_by_id(post_id, posts)
    if not post:
        return "Beitrag nicht gefunden", 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        save_blog_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='update', post=post)

# Beitrag löschen
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Löscht einen Blogbeitrag anhand seiner ID."""
    posts = load_blog_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_blog_posts(posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)