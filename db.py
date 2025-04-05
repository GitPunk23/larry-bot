import sqlite3

def init_db():
    conn = sqlite3.connect('discord_minecraft.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_links (
        discord_id TEXT PRIMARY KEY,
        minecraft_id TEXT
    )
    ''')
    conn.commit()
    conn.close()

def link_user(discord_id, minecraft_id):
    conn = sqlite3.connect('discord_minecraft.db')
    c = conn.cursor()
    c.execute('''
    INSERT OR REPLACE INTO user_links (discord_id, minecraft_id)
    VALUES (?, ?)
    ''', (discord_id, minecraft_id))
    conn.commit()
    conn.close()

def get_minecraft_id(discord_id):
    conn = sqlite3.connect('discord_minecraft.db')
    c = conn.cursor()
    c.execute('''
    SELECT minecraft_id FROM user_links WHERE discord_id = ?
    ''', (discord_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
