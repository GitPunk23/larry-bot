import sqlite3
from dotenv import load_dotenv
import os
import logging

load_dotenv()
DB_PATH = os.getenv('DB_PATH')

if DB_PATH == ":memory:":
    DB_PATH = "file:memdb1?mode=memory&cache=shared"
    conn = sqlite3.connect(DB_PATH, uri=True)
else:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

c = conn.cursor()

def init_db():
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        discord_id TEXT PRIMARY KEY,
        java_id TEXT,
        bedrock_id TEXT
    )
    ''')
    conn.commit()

def link_user(discord_id, java_id=None, bedrock_id=None):
    try:
        if java_id:
            c.execute('''
                INSERT INTO users (discord_id, java_id)
                VALUES (?, ?)
                ON CONFLICT(discord_id) DO UPDATE SET
                java_id = excluded.java_id
            ''', (discord_id, java_id))
        if bedrock_id:
            c.execute('''
                INSERT INTO users (discord_id, bedrock_id)
                VALUES (?, ?)
                ON CONFLICT(discord_id) DO UPDATE SET
                bedrock_id = excluded.bedrock_id
            ''', (discord_id, bedrock_id))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error linking user: {e}")
        return False

def get_java_id(discord_id):
    c.execute('''SELECT java_id FROM users WHERE discord_id = ?''', (discord_id,))
    result = c.fetchone()
    return result[0] if result else None

def get_discord_id(java_id):
    c.execute('SELECT discord_id FROM users WHERE java_id = ?', (java_id,))
    result = c.fetchone()
    return result[0] if result else None

def get_discord_id(bedrock_id):
    c.execute('SELECT discord_id FROM users WHERE bedrock_id = ?', (bedrock_id,))
    result = c.fetchone()
    return result[0] if result else None

def get_bedrock_id(discord_id):
    c.execute('SELECT bedrock_id FROM users WHERE discord_id = ?', (discord_id,))
    result = c.fetchone()
    return result[0] if result else None