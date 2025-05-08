from store.base import Store
import sqlite3
from datetime import datetime
import pytz

class SQLiteStore(Store):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}
        db_path = self.config.get("db_path", "store.sqlite")
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                title TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        cursor.close()

    def update_list(self, source_description: str, news: dict[str, str]) -> dict[str, str]:
        cursor = self.conn.cursor()
        
        # Get existing titles
        cursor.execute("SELECT title FROM news WHERE description = ?", (source_description,))
        existing_titles = {row[0] for row in cursor.fetchall()}
        
        # Find new entries
        new_entries = {
            title: url 
            for title, url in news.items() 
            if title not in existing_titles
        }
        
        # Insert new entries with local timezone
        if new_entries:
            local_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            cursor.executemany(
                "INSERT INTO news (description, title, url, created_at) VALUES (?, ?, ?, ?)",
                [(source_description, title, url, local_time) for title, url in new_entries.items()]
            )
            self.conn.commit()
            
        cursor.close()
        return new_entries