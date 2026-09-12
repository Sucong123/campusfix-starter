"""初始化数据库并写入演示数据（全部虚构）。运行: python init_db.py"""
import sqlite3
from pathlib import Path

from app import DATABASE

DEMO_TICKETS = [
    ("教室投影仪无法开机", "A区301", "按下电源键无反应，指示灯不亮。"),
    ("宿舍水龙头漏水", "6号楼512", "洗漱台水龙头持续滴水，无法关紧。"),
    ("实验室空调不制冷", "实验楼B204", "开机后出风为常温，设定16度无效果。"),
    ("走廊灯闪烁", "教学楼3层", "走廊灯管间歇性闪烁，影响通行。"),
    ("图书馆电脑蓝屏", "图书馆2层电子阅览区", "编号08的电脑开机后蓝屏，无法进入系统。"),
]


def main():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    with open(Path(__file__).parent / "schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.executemany(
        "INSERT INTO tickets (title, room, description) VALUES (?, ?, ?)",
        DEMO_TICKETS,
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    print(f"数据库初始化完成: {DATABASE}")
    print(f"演示工单数量: {count}")
    conn.close()


if __name__ == "__main__":
    main()
