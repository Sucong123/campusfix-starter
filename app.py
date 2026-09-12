"""CampusFix 校园报修工单系统 - Flask 入口"""
import logging
import os
import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

# 项目根目录（本文件所在目录）
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE = Path(os.environ.get("DATABASE_PATH", INSTANCE_DIR / "campusfix.db"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-secret")

# 基本日志配置：输出到 stdout，格式含时间与级别
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("campusfix")


def get_db():
    """获取当前请求的数据库连接（Flask g 对象缓存）"""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/health")
def health():
    """健康检查接口：Docker/CI/部署验证用"""
    return {"status": "ok"}


@app.route("/")
def index():
    db = get_db()
    tickets = db.execute(
        "SELECT id, title, room, status, created_at FROM tickets ORDER BY created_at DESC"
    ).fetchall()
    return render_template("index.html", tickets=tickets)


@app.route("/tickets/<int:ticket_id>")
def ticket_detail(ticket_id):
    db = get_db()
    ticket = db.execute(
        "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
    ).fetchone()
    if ticket is None:
        return render_template("404.html"), 404
    return render_template("detail.html", ticket=ticket)


@app.route("/tickets/new", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        room = request.form.get("room", "").strip()
        description = request.form.get("description", "").strip()
        db = get_db()
        db.execute(
            "INSERT INTO tickets (title, room, description) VALUES (?, ?, ?)",
            (title, description, room),
        )
        db.commit()
        logger.info("created ticket: %s (%s)", title, room)
        return redirect(url_for("index"))
    return render_template("new.html")


if __name__ == "__main__":
    # 仅开发用途；生产部署使用 gunicorn（第11次课）
    app.run(host="127.0.0.1", port=5000, debug=True)
