
# Donation Matcher (Simple Full‑Stack Demo)

A minimal, presentation-ready project that shows how AI‑style scoring can prioritize people in need and match them with donors.

- **Backend:** Flask + SQLite + CORS (Python)
- **Frontend:** Static HTML + Vanilla JS (fetch API)
- **Scoring Logic:** urgency, income, asset ownership, and requested amount
- **Public Demo:** Deploy backend to Render/Railway/Fly.io and frontend to Netlify/Vercel/GitHub Pages.

## Quick Start (Local)

1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
This starts at http://127.0.0.1:5000

2) Frontend
- Just open `frontend/index.html` in your browser, or serve it (recommended) with e.g.:
```bash
python -m http.server 8080 -d frontend
```
Then visit: http://localhost:8080

3) Configure the frontend to point at your backend by changing `API_BASE` in `frontend/script.js`.

## Deploy

### Backend (Render)
- Create a new Web Service from this `backend` folder.
- Set **Start Command**: `gunicorn app:app`
- Add environment variable `PYTHON_VERSION=3.11` (optional).
- After deploy, copy your Render URL (e.g., https://your-app.onrender.com) and set it in `frontend/script.js` as `API_BASE`.

### Frontend (Netlify)
- Drag & drop the `frontend` folder on Netlify, or set it as the publish directory in a new site.
- Update `API_BASE` to your backend URL.
- Done!

## API Endpoints

- `POST /api/victims` — add a person in need
- `POST /api/donors` — add a donor
- `GET /api/victims` — list victims
- `GET /api/donors` — list donors
- `DELETE /api/reset` — wipe DB (demo convenience)
- `GET /api/matches` — compute matches with scores

