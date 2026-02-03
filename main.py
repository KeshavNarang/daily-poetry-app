from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import datetime
import os

app = FastAPI()

# Step 1: Enable CORS so React dev server can fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 2: Backend logic
AUTHORS = [
    "Emily Dickinson",
    "Walt Whitman",
    "John Keats"
]

POETRYDB_BASE = "https://poetrydb.org/author/"

def get_poem_for_today():
    today = datetime.datetime.utcnow().date()
    days_since_epoch = (today - datetime.date(1970, 1, 1)).days

    author_index = days_since_epoch % len(AUTHORS)
    author = AUTHORS[author_index]

    url = f"{POETRYDB_BASE}{author.replace(' ', '%20')}"

    try:
        resp = requests.get(url, timeout=5)
        # Print raw text from PoetryDB
        print("PoetryDB raw response:", resp.text)
        resp.raise_for_status()
        poems = resp.json()
    except Exception as e:
        print("PoetryDB fetch failed:", e)
        poems = [{"title": "Unavailable", "author": author, "lines": ["Poem not available today."]}]

    # Validate response is a list
    if not isinstance(poems, list) or len(poems) == 0:
        print("PoetryDB returned unexpected JSON:", poems)
        poems = [{"title": "Unavailable", "author": author, "lines": ["Poem not available today."]}]

    poem_index = days_since_epoch % len(poems)
    poem = poems[poem_index]

    # Convert lines → stanzas
    stanzas = []
    current_stanza = []
    for line in poem.get("lines", []):
        if line.strip() == "":
            if current_stanza:
                stanzas.append(current_stanza)
                current_stanza = []
        else:
            current_stanza.append(line)
    if current_stanza:
        stanzas.append(current_stanza)

    return {
        "title": poem.get("title", "Untitled"),
        "author": poem.get("author", author),
        "stanzas": stanzas
    }

# Step 3: API route (serve first!)
@app.get("/api/poem")
def get_poem():
    return {
        "date": datetime.date.today().isoformat(),
        "poem": get_poem_for_today()
    }

# Step 4: Serve React frontend build (catch-all)
FRONTEND_DIR = "frontend_build"

if os.path.isdir(FRONTEND_DIR):
    # Serve static files (JS/CSS)
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")
    # Serve all other frontend files (index.html, manifest.json, favicon.ico, logos)
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
