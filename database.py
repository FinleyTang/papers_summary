import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY,
            title TEXT,
            authors TEXT,
            summary TEXT,
            link TEXT,
            updated TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_papers():
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM papers')
    papers = c.fetchall()
    conn.close()
    return papers

def save_papers(papers):
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.executemany('''
        INSERT INTO papers (title, authors, summary, link, updated)
        VALUES (?, ?, ?, ?, ?)
    ''', papers)
    conn.commit()
    conn.close()

def needs_update():
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('SELECT MAX(updated) FROM papers')
    last_updated = c.fetchone()[0]
    conn.close()

    if last_updated is None:
        return True

    last_updated_date = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')
    return datetime.now() - last_updated_date > timedelta(hours=24)