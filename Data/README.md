# FastAPI CRUD Demo

This project is a simple CRUD (Create-Read-Update-Delete) application built with **FastAPI** and SQLAlchemy.

---

## 1. Requirements

* Python 3.9 or newer (Windows, macOS, Linux)
* Git (optional – if you cloned the repo rather than downloaded a .zip)

> **Tip for Windows users:** If you are not sure whether Python is installed, open *PowerShell* and run `python --version`.

---

## 2. First-time setup

1. **Create & activate a virtual environment** (recommended):
   ```powershell
   # From the project root (same folder that contains run_server.bat)
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. **Install dependencies** (they are listed in `fastapi_crud/requirements.txt`):
   ```powershell
   pip install -r fastapi_crud\requirements.txt
   ```
3. **Run the application**:
   *Windows*: double-click `run_server.bat` **or** execute it in *cmd/PowerShell*:
   ```powershell
   .\run_server.bat
   ```
   The script tries to bind to port **8000**. If that port is busy, it automatically picks a random free port (between 10000-60000) and prints the chosen port in the console.

---

## 3. Accessing the app

* Open your browser at the URL shown in the terminal, for example:
  * `http://localhost:8000/`  – main page
  * `http://localhost:8000/docs` – automatic Swagger UI docs

If the script fell back to a random port, replace `8000` with the printed port number.

---

## 4. Stopping the server

Press `Ctrl + C` in the terminal window where the server is running. The database file `sql_app.db` will persist between runs.

---

## 5. Running on Linux / macOS

Instead of the batch file, run:
```bash
uvicorn fastapi_crud.main:app --host 0.0.0.0 --port 8000
```
Add `--reload` for auto-reload during development.

---

## 6. Common issues

* **Port already in use** – The script chooses another port automatically. Make sure to open the correct URL.
* **`pip`/`venv` not found** – Ensure Python is correctly installed and added to your *PATH* environment variable.

---

Enjoy building with FastAPI!
