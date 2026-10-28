# 任务三：命令行贪吃蛇提交材料

克隆或下载本仓库后，在仓库根目录打开 PowerShell。需要 Python 3.10+，无需安装第三方依赖。

```powershell
python snake/main.py
```

WASD 或方向键移动，吃到 `*` 后增长并加分，撞墙或撞自己结束。P 暂停，+/- 调速，Q 退出。

## 实验复现

```powershell
python -m unittest discover -s snake/tests -v
python snake/main.py --demo --seed 7
python -m compileall snake
```

- `snake/`：完整源代码、13 个单元测试、运行说明和本项目 SKILL.md。
- [任务三实验报告](报告/任务三实验报告.md)：任务目标、问题发现、反馈与修改、验证结果、AI 使用说明。
- `实验结果/`：打包前重新执行的测试、演示、入口与编译检查原始日志，环境及结果汇总；历史 PTY 交互单独标为摘要。
- `文件清单与校验.json`：除清单自身外的各文件 SHA-256，用于核对附件。

本次代码生成、测试和 PTY 交互由 AI 执行；没有将其写成用户本人手动操作。原有 PPT 和图片未包含在本作业包中。
