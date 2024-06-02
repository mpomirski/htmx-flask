import sqlite3
from typing import Any
from flask import Flask, render_template, g

app: Flask = Flask(__name__)
DATABASE: str = 'db/database.db'


def get_db() -> sqlite3.Connection:
    db: sqlite3.Connection = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(error) -> None:
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def home() -> str:
    cur: sqlite3.Cursor = get_db().cursor()
    posts: list[Any] = cur.execute('SELECT * FROM posts').fetchmany(10)
    return render_template('home/index.html', posts=posts)


@app.route("/post/<string:post_id>")
def show_post(post_id: str) -> str:
    cur: sqlite3.Cursor = get_db().cursor()
    post: sqlite3.Row = cur.execute(
        'SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    return render_template('home/_partials/show.html', post=post)


if __name__ == '__main__':
    app.run()
