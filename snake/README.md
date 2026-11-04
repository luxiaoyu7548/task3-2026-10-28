# 命令行贪吃蛇

使用 Python 标准库实现，Python 3.10+ 即可运行，无需安装第三方依赖。

## 运行与游玩

在仓库根目录运行：

```powershell
python snake/main.py
```

也可以进入本目录执行 `python main.py`。

| 按键 | 操作 |
| --- | --- |
| 回车 / 空格 | 从 READY 开始 |
| 方向键 | 移动 |
| 空格 | 暂停 / 恢复 |
| `+` / `=`、`-` | 加速、减速，面板同步显示速度 |
| 回车 | GAME OVER 或 YOU WIN 后再来一局 |
| Esc | 退出 |
| WASD、P、Q | 英文输入状态下的移动、暂停、退出快捷键 |

中文输入状态可直接使用方向键、空格和 Esc。若字母键调出了候选框，先按 Esc 取消候选，再操作游戏。

`@` 为蛇头，`o` 为蛇身，`*` 为食物。吃到食物增长并加 1 分；撞墙或撞到自身结束。暂停显示 PAUSED，重玩后恢复 0 分、3 格初始蛇身。

## 演示与测试

```powershell
python main.py --demo --seed 7
python -m unittest discover -s snake/tests -v
```

单元测试命令在仓库根目录执行，完整套件共 18 项。

固定演示结果：

```text
DEMO seed=7 steps=4 score=1 length=4 status=playing
```

## 文件

- `game.py`：移动、食物、计分与碰撞规则。
- `cli.py`：窗口画面、按键、暂停、速度与重玩。
- `main.py`：命令行入口。
- `tests/`：规则与交互回归测试。
- `SKILL.md`：Using Superpowers 项目执行规则。
- [实验报告](../报告（word+md）/任务三实验报告.md)与[窗口游玩记录](../实验结果/窗口游玩记录.md)：问题、反馈、修改和实际游玩截图。
