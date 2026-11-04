# 任务三：命令行贪吃蛇

项目仓库：[luxiaoyu7548/task3-2026-10-28](https://github.com/luxiaoyu7548/task3-2026-10-28)

克隆或解压后，在根目录打开 PowerShell。需要 Python 3.10+，只使用标准库。

```powershell
python snake/main.py
```

- 回车或空格开始；方向键移动。
- 空格暂停或恢复；`+` / `-` 调速，画面显示当前速度。
- 撞墙后按回车重玩；Esc 退出。
- 英文输入状态下也支持 WASD、P 暂停、Q 退出。中文输入状态可使用方向键、空格、Esc。

[任务三实验报告](报告（word+md）/任务三实验报告.md)记录实际游玩中发现的问题、反馈与修复，同文件夹提供内容一致的 [Word 版](报告（word+md）/任务三实验报告.docx)；[窗口游玩记录](实验结果/窗口游玩记录.md)附 25 张原始窗口截图。

## 复现检查

```powershell
python -m unittest discover -s snake/tests -v
python snake/main.py --demo --seed 7
python -m compileall snake
```

最终 18 项测试通过。`snake/` 保存代码和说明，`实验结果/` 保存游玩截图与运行日志，`文件清单与校验.json` 提供文件校验。
