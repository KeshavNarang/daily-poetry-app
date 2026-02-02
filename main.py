from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import datetime
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTHORS = [
    "Emily Dickinson",
    "Walt Whitman",
    "Robert Frost",
    "John Keats",
    "Maya Angelou"
]

POETRYDB_BASE = "https://poetrydb.org/author/"

def get_poem_for_today():
    today = datetime.date.today()
    days_since_epoch = (today - datetime.date(1970, 1, 1)).days
    author_index = days_since_epoch % len(AUTHORS)
    author = AUTHORS[author_index]

    url = f"{POETRYDB_BASE}{author.replace(' ', '%20')}"
    resp = requests.get(url)
    poems = resp.json()
    poem_index = days_since_epoch % len(poems)
    poem = poems[poem_index]

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

# ---- Serve React frontend ----
frontend_path = "frontend_build"

# Mount static files (JS/CSS/assets)
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Serve index.html at root
@app.get("/")
def serve_react():
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)

# ---- API endpoint for poem JSON ----
@app.get("/api/poem")
def poem_api():
    return {
        "date": datetime.date.today().isoformat(),
        "poem": get_poem_for_today()
    }
