
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import string
import random

DB_PATH = "links.db"

app = FastAPI(title="URL Shortener")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_id TEXT UNIQUE,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
        '''
    )
    conn.commit()
    conn.close()

init_db()

class ShortenRequest(BaseModel):
    url: str

def generate_short_id(length: int = 6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

@app.post("/shorten")
def shorten_link(req: ShortenRequest):
    conn = get_conn()
    cur = conn.cursor()

    short_id = generate_short_id()

    cur.execute(
        "INSERT INTO links (short_id, original_url, clicks) VALUES (?, ?, 0)",
        (short_id, req.url),
    )

    conn.commit()
    conn.close()

    return {"short_id": short_id, "short_url": f"/{short_id}"}


@app.get("/{short_id}")
def redirect(short_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT original_url, clicks FROM links WHERE short_id=?", (short_id,))
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Link not found")

    url, clicks = row

    cur.execute(
        "UPDATE links SET clicks=? WHERE short_id=?",
        (clicks + 1, short_id),
    )
    conn.commit()
    conn.close()

    return RedirectResponse(url)


@app.get("/stats/{short_id}")
def stats(short_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT clicks FROM links WHERE short_id=?", (short_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"short_id": short_id, "clicks": row[0]}
