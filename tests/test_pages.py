"""页面级测试（课15）：用 Flask 测试客户端模拟浏览器，不用开服务器。

路由名以本项目 app.py 为准：/tickets/new（新建）、/tickets/<id>（详情），
不是指导书示例里的 /create、/ticket/1。
"""


def test_index(client):
    """首页应返回 200 并含 CampusFix 标题"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix" in resp.data.decode()


def test_detail(client):
    """详情页：先建一条工单，再访问它的详情页（临时库是空的，自给自足）"""
    client.post(
        "/tickets/new",
        data={"title": "详情页测试单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    resp = client.get("/tickets/1")
    assert resp.status_code == 200
    assert "详情页测试单" in resp.data.decode()


def test_create(client):
    """创建工单：POST 后跟随跳转，首页应出现新工单"""
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "测试工单" in resp.data.decode()
