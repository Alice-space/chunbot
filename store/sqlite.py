from store.base import Store, StoreConfig
import sqlite3
import logging

from type import News

logger = logging.getLogger(__name__)


class SqliteStoreConfig(StoreConfig, total=False):
    db_path: str


class SQLiteStore(Store):
    # Base of datasource
    def __init__(self, config: SqliteStoreConfig | None = None):
        super().__init__(config)
        db_path: str = str(self.config.get("db_path", "store.sqlite"))
        logger.info(f"Initializing SQLite database at {db_path}")
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        logger.debug("Initializing database tables")
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()
        cursor.close()
        logger.debug("Database tables initialized")

    def update_list(self, news: list[News]) -> list[News]:
        """Update database with new news items, skipping existing ones.
        Returns the list of news items that were actually inserted."""
        inserted: list[News] = []
        logger.info(f"Processing {len(news)} news items for update")

        for item in news:
            if not item["success"]:
                inserted.append(item)
                continue
            # Check if item exists (by unique title)
            cursor = self.conn.execute(
                "SELECT 1 FROM news WHERE title = ? AND source = ?",
                (item["title"], item["source"]),
            )

            if not cursor.fetchone():
                # Insert new item
                self.conn.execute(
                    """
                    INSERT INTO news (source, title, url, created_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (item["source"], item["title"], item["url"]),
                )
                logger.debug(f"Inserted news item: {item['title']} from {item['source']}")
                inserted.append(item)

        self.conn.commit()
        logger.info(f"Inserted {len(inserted)} new items")
        return inserted
