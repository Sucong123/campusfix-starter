#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_env.py —— 环境体检脚本（第1次课 第三步）

用法（在 VS Code 的 PowerShell 终端里，先 cd 到项目文件夹）：
    py check_env.py
如果 py 不可用，改用：
    python check_env.py

脚本依次检查 6 个工具，每项输出 [通过] 或 [需处理]，
最后统计一共有几项需要处理。
"""

import shutil
import subprocess
import sys

# Windows 上 Python 往管道里写东西时，默认用系统编码（简体中文是 GBK），
# 中文和箭头会变成乱码。这里固定成 UTF-8，和 VS Code 终端保持一致。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

# 微软商店的"假" python.exe 装在这个目录下：能被文件搜索找到，
# 但一运行就跳转到微软商店，所以单独识别出来，不能当成真的 Python。
STORE_PYTHON_DIR = "windowsapps"

# 每项最多等 15 秒，避免某个命令卡住整个脚本
TIMEOUT_SEC = 15


def run(cmd):
    """执行一条命令，返回 (是否可用, 第一行输出 或 错误说明)。

    第二个返回值有三种情况：
      - 命令正常   ：第一行输出，例如 "git version 2.55.0.windows.5"
      - 命令不存在 ：None
      - 特殊错误   ：错误说明字符串（如 "STORE"）
    """
    path = shutil.which(cmd[0])
    if path is None:
        return False, None

    if STORE_PYTHON_DIR in path.lower():
        return False, "STORE"

    # Windows 上 VS Code 的 code 其实是 code.cmd，得借 cmd.exe 才能执行
    if path.lower().endswith((".cmd", ".bat")):
        cmd = ["cmd.exe", "/c"] + cmd

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, str(exc)

    # ssh -V 把版本信息写到 stderr，其它工具写到 stdout，两边都收一下
    out = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    if not out:
        return False, "命令没有输出"
    return True, out.splitlines()[0].strip()


def check(primary, fallback=None, hint=""):
    """检查一个工具。primary 是推荐命令，fallback 是备选命令（如 py 换成 python）。"""
    ok, out = run(primary)
    if ok:
        return " ".join(primary), True, out

    if fallback is not None:
        ok2, out2 = run(fallback)
        if ok2:
            # 备选命令能用也算通过，但显示实际用的是哪条
            return " ".join(fallback), True, out2

    if out == "STORE":
        return " ".join(primary), False, "跳到了微软商店 —— 不是真正的 Python，请重装并勾选 Add Python to PATH"
    return " ".join(primary), False, hint or "未找到，请安装或配置命令行"


def main():
    results = [
        check(["git", "--version"],
              hint="未找到，请安装 Git 后重开终端"),
        check(["py", "--version"], fallback=["python", "--version"],
              hint="未找到，请安装 Python 并勾选 Add Python to PATH"),
        check(["py", "-m", "pip", "--version"], fallback=["python", "-m", "pip", "--version"],
              hint="未找到，请重新安装 Python 并勾选 pip"),
        check(["code", "--version"],
              hint="未找到，请重装 VS Code 并勾选「添加到 PATH」"),
        check(["ssh", "-V"],
              hint="未找到，请在 设置→系统→可选功能 里安装 OpenSSH 客户端"),
        # 用 curl.exe 而不是 curl：PowerShell 里 curl 是 Invoke-WebRequest 的别名
        check(["curl.exe", "--version"], fallback=["curl", "--version"],
              hint="未找到，可用 winget install curl 安装"),
    ]

    width = max(len(cmd) for cmd, _, _ in results) + 2
    failed = 0

    print()
    for cmd, ok, detail in results:
        if ok:
            print("[通过]   {0} → {1}".format(cmd.ljust(width), detail))
        else:
            failed += 1
            print("[需处理] {0} → {1}".format(cmd.ljust(width), detail))

    print()
    if failed == 0:
        print("全部 {0} 项通过，环境没问题。".format(len(results)))
    else:
        print("共 {0} 项，其中 {1} 项需要处理 —— 先别急着下载安装，把报错问老师或脱敏后问 AI。".format(
            len(results), failed))
    print()
    print("提示：上面用的是 curl.exe。在 PowerShell 里直接敲 curl --version 会报错，")
    print("      因为 curl 是 Invoke-WebRequest 的别名，不是真正的 curl。")


if __name__ == "__main__":
    main()
