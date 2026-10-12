import pytest

from app import validate_ticket


def test_title_too_long():
    error = validate_ticket("A" * 21, "A101")
    assert error == "标题不能超过20个字符"


def test_post_title_too_long(client):
    """请求级测试（课15）：用真实 POST 验证同一个规则，路由应拒绝并返回 400"""
    resp = client.post(
        "/tickets/new",
        data={"title": "A" * 21, "room": "A区101", "description": "测试"},
    )
    assert resp.status_code == 400
    assert "标题不能超过20个字符" in resp.data.decode()


@pytest.mark.parametrize("title,expected", [
    pytest.param("正常标题", 200, id="正常标题-200"),
    pytest.param("A" * 19, 200, id="A*19-200"),    # 边界内
    pytest.param("A" * 20, 200, id="A*20-200"),    # 恰好上限
    pytest.param("A" * 21, 400, id="A*21-400"),    # 越界
    pytest.param("A" * 100, 400, id="A*100-400"),  # 无效类代表值
])
def test_title_boundary(client, title, expected):
    """边界值测试（课16）：19/20/21 是标题长度限制的关键边界。

    成功时路由会 302 跳回列表页，故 follow_redirects=True 跟到 200；
    被拒绝的 400 不是重定向，不受影响。
    """
    resp = client.post(
        "/tickets/new",
        data={"title": title, "room": "A区101", "description": "测试"},
        follow_redirects=True,
    )
    assert resp.status_code == expected
