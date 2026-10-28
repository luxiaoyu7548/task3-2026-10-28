---
name: snake-game-using-superpowers
description: 用真实运行反馈驱动一个可验证的命令行贪吃蛇交付
---

# Using Superpowers

本项目按 Using Superpowers 的工作循环执行：

1. 先读清任务约束，明确 Python、命令行、零第三方依赖、独立目录和 README 验收条件。
2. 先写设计文档，再拆实现计划；不把“代码看起来合理”当作完成。
3. 遵守测试先行：先写一个会失败的行为测试，实际看到失败，再写最小实现让它通过。
4. 把规则核心与终端 I/O 分开，让移动、吃食物、增长、计分、撞墙和自撞可以稳定复现。
5. 除单元测试和固定 `--demo` 外，必须打开真实终端按键运行，观察真实输出和退出行为。
6. 发现问题时记录完整症状、命令和输出，反馈到实现决策，再写回归测试修复；不只写“还是不行”。
7. 最后重新运行完整测试、演示、编译检查和真实终端验收，并把证据写入文件。

## 本项目的验证命令

```powershell
python -m unittest discover -s snake/tests -v
python snake/main.py --demo --seed 7
python -m compileall snake
```

## 判断标准

“完成”只在真实结果满足以下条件时成立：蛇会动；吃到食物会增长且分数增加；撞墙或撞自己会结束；README 能让别人从零运行；真实终端按键和退出路径都验证过。
