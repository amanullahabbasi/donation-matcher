
# Backend

Flask + SQLite API for donation matching.

## Run Locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The server listens on `http://127.0.0.1:5000`.

## Deploy (Render)

- New Web Service, use this folder.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- After deploy, note your base URL and put it in `frontend/script.js` as `API_BASE`.
