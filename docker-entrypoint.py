"""容器启动入口：首次启动时初始化数据库，然后启动 Flask 应用。

数据库文件放在 Volume 挂载的目录（/app/data）里，所以删容器不会丢数据。
"""
import os
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", "instance/campusfix.db"))

if not DATABASE_PATH.exists():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.executescript(
        Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    )
    conn.commit()
    conn.close()
    print(f"数据库不存在，已初始化空库: {DATABASE_PATH}", flush=True)

os.execvp("python", ["python", "app.py"])
