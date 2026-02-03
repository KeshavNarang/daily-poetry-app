# Daily Poetry App

A web app that shows a deterministic "poem of the day" from a curated list of authors.  
Built with **React** (frontend) and **FastAPI** (backend), hosted on **Railway**.

---

## Features

- Daily poem with title, author, and stanzas.
- Deterministic selection based on UTC date.
- Handles missing authors gracefully.
- React frontend served as static files through FastAPI.

---

## Project Structure

poems/
- main.py # FastAPI backend
- requirements.txt # Python dependencies
- frontend_build/ # Built React frontend
- daily-poem-frontend/ # React source code


---

## How It Works

1. React frontend fetches `/api/poem` from FastAPI.
2. FastAPI determines the author and poem based on the UTC date.
3. FastAPI fetches poems from PoetryDB.
4. Frontend displays the poem with formatted stanzas.
5. If a poem is unavailable, a fallback message is shown.

---

## Setup

### Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```cd daily-poem-frontend
npm install
npm start

Build for Production
npm run build
# Copy build into frontend_build/ for FastAPI to serve
```

### Deployment

Push the repo to Railway.

FastAPI serves both the API (/api/poem) and the static frontend (/).

### Notes
Uses UTC date for deterministic daily selection.
Only authors available in PoetryDB are included.
Simple inline CSS for readability.
Works locally and on Railway without extra configuration.
