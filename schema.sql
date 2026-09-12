-- CampusFix 建表 SQL
DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    room TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',      -- open / in_progress / closed
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
