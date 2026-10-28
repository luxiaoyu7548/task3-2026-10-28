# 命令行贪吃蛇

这是任务三的可运行成果：一个只使用 Python 标准库的 ASCII 命令行贪吃蛇。

## 环境与依赖

- Python 3.10 或更高版本（本次验收使用 Python 3.13.15）。
- 不需要 `pip install`，没有第三方依赖。
- 如果电脑没有 Python，请从 <https://www.python.org/downloads/> 安装 Python 3.10+，Windows 安装器中勾选 **Add Python to PATH**，然后重新打开 PowerShell。

## 运行

在工作区根目录执行：

```powershell
python snake/main.py
```

也可以进入独立目录后执行：

```powershell
cd snake
python main.py
```

键位：

- `WASD` 或方向键：移动。
- `P`：暂停/继续。
- `+` / `=`：加速；`-`：减速。
- `Q` 或 `Ctrl+C`：退出。

蛇吃到 `*` 后会变长并加 1 分；`@` 是蛇头，`o` 是蛇身。撞墙或撞到自己会结束，终端会保留最终分数。

## 可复现演示与测试

不需要键盘输入的演示：

```powershell
python snake/main.py --demo --seed 7
```

预期输出类似：

```text
DEMO seed=7 steps=4 score=1 length=4 status=playing
```

运行单元测试：

```powershell
python -m unittest discover -s snake/tests -v
```

编译检查：

```powershell
python -m compileall snake
```

## 目录

- `game.py`：棋盘、移动、食物、计分和碰撞规则。
- `cli.py`：ASCII 渲染、键盘读取、暂停和速度控制。
- `main.py`：命令行入口与 `--demo`。
- `tests/`：规则和 CLI 行为测试。
- `SKILL.md`：本次使用 Using Superpowers 的工作约束。
- [任务三实验报告](../报告/任务三实验报告.md)：问题发现、反馈和修复记录。
