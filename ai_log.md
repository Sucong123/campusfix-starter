# AI工程日志

> 本文件记录我使用 AI 的过程，是课程的过程证据之一。
> **脱敏规则**：服务器IP写 `<SERVER_IP>`，用户名写 `<USER>`，Token写 `<TOKEN_REDACTED>`，私钥一律不粘贴。

---

## 记录1（日期：2026-09-12，实验：第1次）

- **我原来的目标**：
  完成第1次课第三步的「环境体检」，确认这台电脑上的 Git、Python、pip、VS Code、SSH、curl 六个工具都能用；缺哪个就补哪个，最后填出体检结果表。

- **我提供给AI的信息（已脱敏）**：
  实验指导书在我电脑上的本地文件路径（`D:\下载\02-实验指导书-学生版 (4).md`）。
  **没有**提供任何密码、Token、私钥、服务器地址或真实个人信息。

- **提示词摘要**：
  「把这份实验指导书读一遍，帮我跑一遍第三步的环境体检，把结果整理成表格；顺便看看有没有会影响后面课程的环境问题。」

- **AI建议摘要**：
  1. 在 PowerShell 里逐条执行 `git --version`、`py --version`、`py -m pip --version`、`code --version`、`ssh -V`、`curl --version`，把六项结果整理成表。
  2. 提醒：`curl --version` 在 Windows PowerShell 5.1 里会报错，因为 `curl` 是 `Invoke-WebRequest` 的别名；真正的 curl 要用 `curl.exe --version`。这不是环境问题。
  3. 发现本机 Python 是 3.14.4，而第2次课的指导书里写的是 `py -3.13 -m venv .venv`——执行那句会报 `No suitable Python runtime found`，到时候要去掉 `-3.13`。
  4. 发现指导书里说"老师会提供"的 `check_env.py` 在本机没找到，于是写了一份等价的替代脚本。

- **我采纳/拒绝的部分及理由**：
  - **采纳**：六项命令逐条执行。—— 指导书第三步明确要求的，本身就是任务。
  - **采纳**：`curl.exe` 的说明。—— 我自己在终端里试了一遍：`curl --version` 报错，错误信息末尾写着 `[Invoke-WebRequest]`，证明执行的确实不是真正的 curl；换成 `curl.exe --version` 就正常输出 `curl 8.21.0`。AI的解释和实际现象对得上，所以采信。
    （注：AI 一开始预测的报错文字和我实际看到的**不完全一样**——AI说会报 Uri 类型转换错，我实际看到的是 `未能解析此远程名称: '--version'`。因为 AI 是在脚本里用数组参数调用的，我在终端直接敲是字符串，走的代码路径不同。但"curl 是 Invoke-WebRequest 的别名"这个核心结论是对的，而且我看到的错误信息里直接出现了 `[Invoke-WebRequest]`，反而更直接地证明了这一点。）
  - **采纳**：`check_env.py` 替代脚本。—— 老师那份暂时没找到，先有一份能跑通的，不影响流程。
  - **暂不采纳**：Python 3.13 的事。—— 那是第2次课才会踩到的，现在不动，先记下来。

- **我实际执行的操作**：
  在 VS Code 里打开项目文件夹 `C:\Users\23013\Desktop\campusfix-starter`，用 PowerShell 终端（菜单：终端 → 新建终端）执行：
  ```powershell
  py check_env.py
  ```
  这个脚本内部会依次调用下面六条命令，并把结果打印出来：
  `git --version`、`py --version`、`py -m pip --version`、`code --version`、`ssh -V`、`curl.exe --version`。
  另外，整个过程中我把实验指导书交给了 AI 让它先读一遍要求——**没有**把任何密码、Token、私钥、服务器地址或真实个人信息交给它。

- **验证命令/结果**：
  执行 `py check_env.py` 后，终端输出（截图见提交的证据）：
  ```text
  [通过]   git --version         → git version 2.55.0.windows.5
  [通过]   py --version          → Python 3.14.4
  [通过]   py -m pip --version   → pip 26.0.1 from C:\Users\23013\AppData\Local\Programs\Python\Python314\Lib\site-packages\pip (python 3.14)
  [通过]   code --version        → 1.136.2
  [通过]   ssh -V                → OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2
  [通过]   curl.exe --version    → curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

  全部 6 项通过，环境没问题。
  ```
  结论：六项全部通过，**本课不需要安装任何软件**。

- **我现在能独立解释的内容**：

  1. **为什么 PowerShell 里的 `curl` 不是真的 curl？**
     因为 PowerShell 5.1 早就把 `curl` 定义成了一个"别名"，指向它自带的 `Invoke-WebRequest`。
     别名的优先级比 PATH 查找更高，所以敲 `curl` 时根本不会去找真正的 `curl.exe`。
     这两个程序参数不兼容：`Invoke-WebRequest` 的第一个位置参数是 `-Uri`，要的是一个网址。
     我把 `--version` 传给它，它就把 `--version` 当成网址去解析，解析不了，所以报 `未能解析此远程名称: '--version'`。
     错误信息末尾的 `[Invoke-WebRequest]` 正好证实了这一点——执行的确实不是 curl。
     写全名 `curl.exe` 就能绕过别名，因为别名只对 `curl` 这个名字生效。

  2. **`py check_env.py` 这条命令里，`py` 是什么？`check_env.py` 是什么？两者是什么关系？**
     `py` 是 Python 启动器（Launcher），是装 Python 时附带的独立小程序，它在 `C:\Windows\py.exe`。
     它的作用是帮我找到电脑上装的 Python 并启动它（我电脑上只有 3.14，用 `py -0` 能列出来）。
     `check_env.py` 是一个脚本文件，里面写着要执行的指令，本质上就是一段文本。
     两者是"执行者"和"被执行的东西"的关系：整条命令就是让 `py` 找到 Python，再让它运行 `check_env.py`。
     （`python check_env.py` 也能跑，但 `python` 是指向某个具体版本的安装，`py` 在装了多个版本时更灵活。）

  3. **这个脚本检查的 6 个工具，分别对应后面课程的哪一环？**
     按指导书第二步的技术栈顺序 Git → Linux → 测试 → CI → Docker：
     - **Git** → 管代码。后面所有协作（Issue → 分支 → PR → Review）都靠它。
     - **Python** → 课程项目的语言。CampusFix 是 Flask 写的，Flask 就是 Python 的库，没它项目跑不起来。
     - **pip** → Python 的包管理器，装第三方库用的（requirements.txt 里的 flask、pytest 都靠它装）。
     - **VS Code** → 写代码的编辑器，也是我运行终端的操作台，后面几乎所有操作都在这里做。
     - **SSH** → 对应 Linux 那一环。远程登录服务器用的，课程后面要连到远程 Linux 机器上操作。
     - **curl** → 对应 CI 那一环。命令行发 HTTP 请求，CI 里常拿它检查服务是不是活着（就像 CampusFix 的 `/health` 接口）。

---

> **交之前的自检**：把上面第 1～3 题的答案**不看稿子念一遍**。
> 能顺口讲出来 = 真的懂了；念得磕磕巴巴 = 回去再看一遍上面的解释，
> 或者直接在课上问老师（课堂核验占 20%，老师很可能当面问到这里）。

---

## 记录2（日期：2026-09-12，实验：第2次）

- **我原来的目标**：
  在自己电脑上把 CampusFix 跑起来（建虚拟环境 → 装依赖 → 初始化数据库 → 启动 → 改页面），
  并完成指导书里"奇怪的现象"那个挑战。

- **我提供给AI的信息（已脱敏）**：
  第2次课实验指导书的本地路径（`D:\下载\02-实验指导书-学生版 (5).md`）、项目目录 `C:\Users\23013\Desktop\campusfix-starter`。
  **没有**提供任何密码、Token、私钥、服务器地址或真实个人信息。

- **提示词摘要**：
  1. 「读这份实验指导书，看看我电脑上有没有这个项目、做到哪一步了。」
  2. 「你帮我建那条工单（位置 `A区301`、描述 `投影仪不亮`）。」

- **AI建议摘要**：
  1. 先查环境状态（`.venv` 是否存在、装了哪些包、`instance/campusfix.db` 是否已生成），再决定从哪步接着做 —— 不要盲目从头重跑。
  2. 用后台进程启动 `app.py`，再用 `curl.exe` 访问 `/health` 和 `/` 验证。
  3. 建工单：`app.py` 只接受 POST，所以用 `curl.exe -X POST` 提交表单。

- **我采纳/拒绝的部分及理由**：
  - **采纳**：先查状态再动手。—— 避免重复建 venv、重复初始化数据库。
  - **采纳**：用 `curl.exe` 验证而不是"看一眼日志觉得没事了"。—— HTTP 状态码是硬证据。
  - **部分采纳**：AI 帮我启动了应用，但我随后**自己**在 VS Code 终端里重新敲了一遍
    `python app.py`，并核对监听端口的进程（PID 17876，启动时间 10:46:16 就是我敲命令的时间）。
    别人替你跑通 ≠ 你会跑。
  - **采纳**：让 AI 提交工单、我去看详情页。—— 指导书要求"先不要改代码"，只观察。

- **我实际执行的操作**：
  在自己的终端（VS Code → PowerShell，提示符带 `(.venv)`）执行 `python app.py`，
  看到 `* Running on http://127.0.0.1:5000` 后，浏览器访问 `/` 和 `/health`，并截图。

- **验证命令/结果**：
  - `curl.exe -s http://127.0.0.1:5000/health` → `{"status": "ok"}`
  - `Get-NetTCPConnection -LocalPort 5000 -State Listen` → 确认监听进程是我的 python
  - 新建工单的详情页（`/tickets/6`）：位置栏显示 投影仪不亮，描述栏显示 A区301。
    - 新建工单的详情页（`/tickets/6`）：位置栏显示 投影仪不亮，描述栏显示 A区301。
    我判断原因：`app.py` 里 SQL 的列名顺序是 `(title, room, description)`，
    但下面的值顺序是 `(title, description, room)` —— 值和列按位置一一对应，
    所以 `description` 的值进了 `room` 列，`room` 的值进了 `description` 列，位置和描述整个调换了。


- **我现在能独立解释的内容**：
  1. **`init_db.py` 为什么能安全地重复运行？**
     因为 `schema.sql` 第一行是 `DROP TABLE IF EXISTS tickets` —— 先删旧表再建新表，最后重新插入 5 条演示数据。
     所以重复执行的结果是**重置**，不是**追加**：表被清空重建，数据回到初始的 5 条。
     （如果脚本写成只 INSERT 不 DROP，跑两次就会变成 10 条。）
  2. **`/health` 这个接口有什么用？**
     它不给人看，给机器看。返回一个固定的 JSON（`{"status": "ok"}`），
     部署脚本、Docker、CI 流水线靠请求它来判断"应用到底活着没有" —— 比人工打开浏览器点一遍可靠得多。
     后面第 11 次课做部署时会真正用上它。
  3. **`(.venv)` 这个提示符前缀意味着什么？**
     表示当前终端的 `python`、`pip` 都指向 `.venv\Scripts\` 里的那一套，不是系统全局的。
     项目依赖装在各自的环境里，不同项目的库就不会互相打架。

---

## 记录3（日期：2026-09-12，实验：第3次）

- **我原来的目标**：
  学会 Git 基本操作：初始化仓库、分多条提交、写 `.gitignore`、按规范写提交消息，最后有一个"干净"的仓库。

- **我提供给AI的信息（已脱敏）**：
  第3次课实验指导书的本地路径（`D:\下载\02-实验指导书-学生版 (6).md`）、项目目录路径。
  **没有**提供任何密码、Token、私钥、服务器地址或真实个人信息。

- **提示词摘要**：
  1. 「读这份指导书，看看我的仓库现在是什么状态、能不能按它写的做。」
  2. 「选 A。」（在"保留老师的初始提交"和"删除 `.git` 重来"之间做的选择）
  3. 「`git diif` 在哪？」（打错字了）

- **AI建议摘要**：
  1. **发现前提冲突**：老师的起始包**自带 `.git` 和一条"初始提交"**，14 个文件已经被跟踪。
     所以指导书第三步的 `git add app.py` / `git add README.md` **不会产生任何提交** ——
     因为这两个文件没被改过，`git add` 加的是"改动"，不是"文件"。
  2. 给两条路：A 保留老师的提交、在此基础上做 3 条新提交；B 删掉 `.git` 完全按指导书重演一遍。
  3. 指出了指导书第四步的验证命令 `git ls-files | grep -E ...` 在 PowerShell 里跑不了（没有 `grep`），
     换成了 `Select-String`。

- **我采纳/拒绝的部分及理由**：
  - **采纳 A 方案**：保留老师的提交，不动别人的历史；我该练的 `add`/`commit`/`status` 一个不少。
  - **采纳**：`grep` → `Select-String` 的替换。—— 我实际敲了 `grep` 报错（PowerShell 里没有这个命令），
    AI 的替换方案和实际症状对得上。
  - **再次采纳**：`.gitignore` 注释从中文改成英文。—— 中文注释在不同编码环境会变成乱码，
    这个我在 PowerShell 里亲眼见过（`Get-Content .gitignore` 输出全是乱码）。
  - **事后调整**：AI 最初给我的三条提交内容（app.py / init_db.py / README.md）**用不了**，
    因为它一开始只看了指导书，没先看仓库实际状态。改成基于真实改动排的三条。

- **我实际执行的操作**：
  在 VS Code 的 PowerShell 终端（项目目录下）依次执行：
  ```powershell
  git add check_env.py
  git commit -m "chore: 添加环境体检脚本"
  git add .gitignore
  git commit -m "chore: .gitignore 注释改用英文，避免跨平台乱码"
  git add templates/index.html
  git commit -m "feat: 首页标题按指导书要求加上小组标识"
  ```

- **验证命令/结果**：
  - `git log --oneline` → 4 条提交（老师的 `eb4bafe` + 我的 `2ccb3d5` / `77c0bf0` / `4367dda`）。
  - `git ls-files | Select-String -Pattern "(\.env|instance)"` → 只匹配到 `.env.example`（模板文件，**本来就该被跟踪**），
    真正的 `.env` 没被跟踪。校验通过。
  - `git check-ignore -v instance/campusfix.db __pycache__ .env` → 精确报出被哪条规则、哪一行忽略，规则确实生效。

- **我现在能独立解释的内容**：
  1. **为什么 `git add` 一个"没改过的已跟踪文件"什么都不会发生？**
     因为 `git add` 处理的是**改动**，不是文件本身。文件已经被跟踪、内容又和上次提交完全一样，
     暂存区里就没有任何东西可加。所以 `git status` 会说 `nothing to commit`。
  2. **`.gitignore` 里的规则前面有空格会怎样？**
     规则会**失效**。我实际踩过这个坑：粘贴的时候所有行前面都多了 2 个空格，
     结果 `git status` 里冒出了 `__pycache__/` 和 `instance/` 两个"未跟踪文件" —— 本该被忽略的东西裸奔了。
     教训：**粘贴完必须用 `git status` 验证**，不能粘完就提交。
  3. **为什么提交时会出现 LF/CRLF 的 warning？**
     我电脑上 `core.autocrlf = true`：提交时把 Windows 的 CRLF 转成 LF 存进仓库，检出时再转回来。
     这个 warning 只是提示"下次 Git 碰这个文件时会转换行尾"，不是错误，不影响内容。
  4. **为什么改一行文字、提交时显示 `1 insertion(+), 1 deletion(-)`？**
     Git 是按"行"记录改动的，不是按字符。改一行 = 删一行 + 加一行。
     如果显示的数字远超你实际改的量，就说明改动范围失控了 —— 所以要养成**提交前先看 `git diff`** 的习惯。
