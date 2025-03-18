from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Funktion zum Laden der Blogbeiträge
def load_blog_posts():
    if os.path.exists('blog_posts.json'):
        with open('blog_posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Funktion zum Speichern der Blogbeiträge
def save_blog_posts(posts):
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

# Startseite
@app.route('/')
def index():
    posts = load_blog_posts()
    return render_template('index.html', posts=posts)

# Neuer Beitrag hinzufügen
@app.route('/add', methods=['GET', 'POST'])
def add():
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
    return render_template('add.html')

# Beitrag aktualisieren
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_blog_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Beitrag nicht gefunden", 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        save_blog_posts(posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

# Beitrag löschen
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_blog_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_blog_posts(posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)