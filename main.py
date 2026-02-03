from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
import datetime

app = FastAPI()

FRONTEND_DIR = "frontend_build"

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

# Step 2: Enable CORS so React dev server can fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
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

    # deterministic author selection
    author_index = days_since_epoch % len(AUTHORS)
    author = AUTHORS[author_index]

    # fetch poems from PoetryDB
    url = f"{POETRYDB_BASE}{author.replace(' ', '%20')}"
    resp = requests.get(url)
    poems = resp.json()

    # deterministic poem selection
    poem_index = days_since_epoch % len(poems)
    poem = poems[poem_index]

    # convert lines → stanzas (empty lines separate stanzas)
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


@app.get("/")
def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "date": datetime.date.today().isoformat(),
        "poem": get_poem_for_today()
    }

@app.get("/api/poem")
def get_poem():
    return {
        "date": datetime.date.today().isoformat(),
        "poem": get_poem_for_today()
    }
