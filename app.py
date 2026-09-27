import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
DATABASE = Path(__file__).with_name("tasks.db")


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, completed INTEGER NOT NULL DEFAULT 0)"
        )


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        action = request.form.get("action")
        task_id = request.form.get("task_id", type=int)

        with sqlite3.connect(DATABASE) as db:
            if action == "add":
                title = request.form.get("title", "").strip()
                if title:
                    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            elif action == "toggle" and task_id:
                db.execute(
                    "UPDATE tasks SET completed = 1 - completed WHERE id = ?",
                    (task_id,),
                )
            elif action == "delete" and task_id:
                db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        return redirect("/")

    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        tasks = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()

    return render_template("index.html", tasks=tasks)


init_db()


if __name__ == "__main__":
    app.run(debug=True)