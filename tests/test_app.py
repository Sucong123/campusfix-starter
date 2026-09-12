"""CampusFix 示例测试。

其中一个测试会暴露起始版本的预置缺陷。请根据失败输出、页面现象和
数据库结果定位问题；不要在尚未复现前直接修改产品代码。
"""


def test_health(client):
    """健康检查接口应返回 ok"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_tickets(client):
    """首页应正常渲染 CampusFix 标题（空库也允许）"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix".encode("utf-8") in resp.data


def test_create_ticket(client):
    """POST 创建工单：列表出现新工单，且 room/description 字段顺序正确"""
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "测试教室", "description": "测试描述"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # 通过：新工单出现在列表中
    assert "测试工单".encode("utf-8") in resp.data
    # 业务要求：列表页显示学生提交的正确位置。
    assert "测试教室".encode("utf-8") in resp.data
