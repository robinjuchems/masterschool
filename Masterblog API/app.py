from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Funktion zum Laden der Posts aus posts.json
def get_posts():
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Funktion zum Speichern der Posts in posts.json
def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

# Route: Alle Beiträge anzeigen (Index)
@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', view='index', posts=posts)

# Route: Einzelnen Beitrag anzeigen
@app.route('/post/<int:post_id>')
def post(post_id):
    posts = get_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return redirect(url_for('index'))
    return render_template('index.html', view='post', post=post)

# Route: Neuen Beitrag hinzufügen
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = get_posts()
        new_id = max([post['id'] for post in posts], default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='add')

# Route: Beitrag aktualisieren
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = get_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='update', post=post)

# Route: Beitrag löschen
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = get_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)