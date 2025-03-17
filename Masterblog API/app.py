from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def get_posts():
    try:
        with open('posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

def fetch_post_by_id(post_id):
    posts = get_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/', methods=['GET'])
def index():
    blog_posts = get_posts()
    return render_template('index.html', view='index', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = get_posts()
        new_id = max([post['id'] for post in posts], default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='add')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = get_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = get_posts()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        posts = [p if p['id'] != post_id else post for p in posts]
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('index.html', view='update', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)