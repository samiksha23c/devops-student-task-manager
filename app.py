import os
import sqlite3
from datetime import date
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "planner.db"))

def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                due_date TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO tasks (title, category, due_date, priority, completed) VALUES (?, ?, ?, ?, ?)",
                [
                    ("Finish DevOps project report", "College", date.today().isoformat(), "High", 0),
                    ("Practice Python problems", "Learning", "", "Medium", 0),
                    ("Review weekly notes", "Personal", "", "Low", 1),
                ],
            )

@app.get("/")
def index():
    with connect_db() as db:
        tasks = db.execute("""
            SELECT * FROM tasks
            ORDER BY completed ASC,
                     CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
                     CASE WHEN due_date = '' OR due_date IS NULL THEN 1 ELSE 0 END,
                     due_date ASC,
                     id DESC
        """).fetchall()
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1").fetchone()[0]
        pending = total - completed
    return render_template("index.html", tasks=tasks, total=total, completed=completed, pending=pending, today=date.today().isoformat())

@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "General").strip() or "General"
    due_date = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "Medium")
    if not title:
        flash("Please enter a task title.", "error")
        return redirect(url_for("index"))
    if len(title) > 160:
        flash("Task title must be 160 characters or fewer.", "error")
        return redirect(url_for("index"))
    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"
    with connect_db() as db:
        db.execute(
            "INSERT INTO tasks (title, category, due_date, priority) VALUES (?, ?, ?, ?)",
            (title, category[:40], due_date, priority),
        )
    flash("Task added successfully.", "success")
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with connect_db() as db:
        task = db.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            flash("Task not found.", "error")
        else:
            db.execute("UPDATE tasks SET completed = ? WHERE id = ?", (0 if task["completed"] else 1, task_id))
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with connect_db() as db:
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    try:
        with connect_db() as db:
            db.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except sqlite3.Error:
        return jsonify({"status": "unhealthy", "database": "error"}), 503

@app.get("/api/tasks")
def api_tasks():
    with connect_db() as db:
        rows = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Database initialized.")

init_db()

if __name__ == "__main__":
    # Development server for local learning only; use a production WSGI server in deployment.
    app.run(host="0.0.0.0", port=5000, debug=False)
