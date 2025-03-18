from flask import Flask, jsonify, request
from flask_cors import CORS

# Flask-App initialisieren
app = Flask(__name__)

# CORS für alle Routen aktivieren
CORS(app)

# In-Memory-Liste der Blogposts
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."}
]

# List-Endpunkt: GET /api/posts
@app.route('/api/posts', methods=['GET'])
def list_posts():
    """Gibt eine Liste aller Blogposts zurück, optional sortiert nach Titel oder Inhalt."""
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    if sort_field:
        if sort_field not in ['title', 'content']:
            return jsonify({"error": "Ungültiges Sortierfeld. Muss 'title' oder 'content' sein."}), 400
        if direction not in ['asc', 'desc']:
            return jsonify({"error": "Ungültige Richtung. Muss 'asc' oder 'desc' sein."}), 400
        reverse = (direction == 'desc')
        posts = sorted(POSTS, key=lambda p: p[sort_field].lower(), reverse=reverse)
    else:
        posts = POSTS

    return jsonify(posts), 200

# Hinzufügen-Endpunkt: POST /api/posts
@app.route('/api/posts', methods=['POST'])
def add_post():
    """Fügt einen neuen Blogpost hinzu und gibt ihn mit einer eindeutigen ID zurück."""
    if not request.is_json:
        return jsonify({"error": "Anfrage muss JSON sein"}), 400

    data = request.get_json()

    if "title" not in data or not data["title"]:
        return jsonify({"error": "Fehlendes Pflichtfeld: title"}), 400
    if "content" not in data or not data["content"]:
        return jsonify({"error": "Fehlendes Pflichtfeld: content"}), 400

    new_id = max([post["id"] for post in POSTS], default=0) + 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

# Löschen-Endpunkt: DELETE /api/posts/<id>
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Löscht einen Blogpost anhand seiner ID."""
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post mit ID {post_id} nicht gefunden"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post mit ID {post_id} wurde erfolgreich gelöscht."}), 200

# Aktualisieren-Endpunkt: PUT /api/posts/<id>
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Aktualisiert einen bestehenden Blogpost anhand seiner ID."""
    if not request.is_json:
        return jsonify({"error": "Anfrage muss JSON sein"}), 400

    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post mit ID {post_id} nicht gefunden"}), 404

    data = request.get_json()
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    return jsonify(post), 200

# Such-Endpunkt: GET /api/posts/search
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Sucht nach Posts anhand von Titel oder Inhalt mittels Query-Parametern."""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    if title_query or content_query:
        filtered_posts = [
            post for post in POSTS
            if (title_query and title_query in post["title"].lower()) or
               (content_query and content_query in post["content"].lower())
        ]
    else:
        filtered_posts = POSTS

    return jsonify(filtered_posts), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)