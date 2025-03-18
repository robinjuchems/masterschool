<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Mein Blog</title>
</head>
<body>
    <h1>Mein Blog</h1>

    {% if view == 'list' %}
        <h2>Alle Beiträge</h2>
        <ul>
            {% for post in posts %}
                <li>
                    <strong>{{ post.title }}</strong> - {{ post.content }}
                    <a href="{{ url_for('delete', post_id=post.id) }}">Löschen</a>
                </li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('add') }}">Neuen Beitrag hinzufügen</a>
    {% elif view == 'add' %}
        <h2>Neuen Beitrag hinzufügen</h2>
        <form method="post" action="{{ url_for('add') }}">
            <label for="title">Titel:</label>
            <input type="text" name="title" id="title" required>
            <br>
            <label for="content">Inhalt:</label>
            <textarea name="content" id="content" required></textarea>
            <br>
            <input type="submit" value="Hinzufügen">
        </form>
        <a href="{{ url_for('index') }}">Zurück zur Liste</a>
    {% endif %}
</body>
</html>