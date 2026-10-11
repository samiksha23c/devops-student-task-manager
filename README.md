# FocusFlow — Study & Task Planner

FocusFlow is a responsive study and daily task planner built with Flask, SQLite, HTML, CSS, and JavaScript. It helps students and individuals record tasks, group them by category, set due dates and priorities, mark work complete, and remove tasks. It is also a DevOps learning project with automated tests, Docker, Docker Compose, and GitHub Actions CI.

## Features
- Responsive task-planner website
- Add task title, category, due date, and priority
- Mark tasks complete or pending
- Delete tasks
- Filter by all, to-do, and completed
- SQLite persistence (tasks survive app restarts when the database file or Docker volume is retained)
- Health endpoint at `/health` and JSON API at `/api/tasks`
- Seven automated tests with pytest
- Docker container and Docker Compose setup
- GitHub Actions runs tests and builds a Docker image on pushes and pull requests to `main`

## Tech stack
Python 3.12, Flask, SQLite, HTML5, CSS3, JavaScript, pytest, Git, GitHub Actions, Docker, Docker Compose.

## Run locally on Windows
1. Install Python 3.12+ and Git.
2. Open PowerShell in this project folder.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If script activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same terminal, then activate again.
4. Install dependencies:
   ```powershell
   python -m pip install -r requirements-dev.txt
   ```
5. Start the website:
   ```powershell
   python app.py
   ```
6. Visit http://127.0.0.1:5000.

Stop the app with Ctrl+C. The local database is `planner.db`.

## Run tests
```powershell
pytest -v
```
The tests use a temporary database so your local tasks are not changed by test runs.

## Run with Docker
Start Docker Desktop, then run:
```powershell
docker compose up --build
```
Open http://localhost:5000. Stop with Ctrl+C, or run `docker compose down`. The named Docker volume `focusflow_data` stores the SQLite database across container recreations. To delete that data intentionally, use `docker compose down -v`.

## Useful endpoints
- `GET /` — website
- `GET /health` — health status and database connectivity
- `GET /api/tasks` — tasks in JSON format

## Upload to GitHub
Create a new empty repository named `focusflow-study-planner` on GitHub. Do not add a README remotely because this project already contains one. Then run these commands from this folder, replacing `YOUR-USERNAME`:
```powershell
git init
git add .
git commit -m "Add FocusFlow DevOps study planner"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/focusflow-study-planner.git
git push -u origin main
```
Open the repository's **Actions** tab to check the CI run. The workflow tests the application and builds an image; it does not publish the image or deploy the site to a public hosting provider.

## CI workflow
1. GitHub Actions checks out the code.
2. It sets up Python 3.12 and installs the development dependencies.
3. pytest runs the automated tests.
4. The Docker build job runs only if the test job succeeds.
5. The Actions tab displays logs and the final result.

## Important notes
This is an educational starter project, not a hardened production service. Before public deployment, set a strong secret key using an environment variable, use a production WSGI server, add authentication and CSRF protection, validate date fields more strictly, and review dependency/security updates. SQLite is suitable for a small single-user demonstration; a multi-user production app may need a managed database.
