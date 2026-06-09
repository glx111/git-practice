"""
============================================
 🧠 日记备份 Agent
============================================

这是你的第一个 Agent 项目！

Agent 循环：Think → Act → Observe → Repeat
不需要任何外部 API，完全本地运行。

作用：
  自动检测日记变化 → 暂存 → 提交 → 推送到 GitHub
"""

import subprocess
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')


# ============================================
# 🧠 Agent 的核心：决策引擎
# ============================================

class DiaryBackupAgent:
    """
    一个简单的 Agent，负责日记备份。

    它有一个循环：
      Think  → 检查状态，决定做什么
      Act    → 执行 git 命令
      Observe → 看结果，判断成功还是失败
      Repeat → 如果失败，想办法处理
    """

    def __init__(self, repo_path):
        self.repo = repo_path
        self.log = []  # Agent 的记忆：记录做过什么

    def run(self, command):
        """Agent 的手：执行命令并观察结果"""
        result = subprocess.run(
            command, shell=True, cwd=self.repo,
            capture_output=True, text=True
        )
        return result.returncode, result.stdout + result.stderr

    # ===== Agent 的四个步骤 =====

    def think(self):
        """步骤 1：思考 —— 看看有没有需要做的事"""
        print("🧠 [Think]  检查 Git 状态...")
        code, output = self.run("git status --short")
        print(f"           {output.strip() or '(没有变化)'}")

        if not output.strip():
            return {"action": "nothing", "reason": "没有变化，无需备份"}

        # 分析哪些文件变化了
        changes = [line.strip() for line in output.strip().split("\n") if line.strip()]
        return {
            "action": "backup",
            "files": changes,
        }

    def act(self, decision):
        """步骤 2：行动 —— 执行 git 三连拍"""
        if decision["action"] == "nothing":
            return {"status": "skip", "msg": decision["reason"]}

        print("🖐  [Act]    执行备份...")

        # Add（暂存）
        print("           git add .")
        code, out = self.run("git add .")
        if code != 0:
            return {"status": "fail", "step": "add", "msg": out}

        # Commit（提交）
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"📝 日记更新 - {now}"
        print(f'           git commit -m "{msg}"')
        code, out = self.run(f'git commit -m "{msg}"')
        if code != 0:
            return {"status": "fail", "step": "commit", "msg": out}

        # Push（推送）
        print("           git push")
        code, out = self.run("git push")
        if code != 0:
            return {"status": "fail", "step": "push", "msg": out}

        return {"status": "success"}

    def observe(self, result):
        """步骤 3：观察 —— 检查结果"""
        print("👀 [Observe] 检查结果...")

        if result["status"] == "skip":
            print(f"           ⏭  {result['msg']}")
        elif result["status"] == "success":
            print("           ✅ 备份成功！日记已安全存到 GitHub")
        elif result["status"] == "fail":
            print(f"           ❌ 失败在 {result['step']} 步骤：{result['msg'][:100]}")

        return result

    def decide_next(self, result):
        """步骤 4：决策 —— 要不要继续？"""
        # 对于这个简单 Agent，不需要重复
        # 但如果是复杂任务，这里可以返回新的 decision
        return None


def main():
    print("=" * 55)
    print("🤖 日记备份 Agent 启动")
    print("=" * 55)
    print()
    print("Agent 循环：Think → Act → Observe → Done")
    print("─" * 55)

    agent = DiaryBackupAgent(os.path.expanduser("~/git-practice"))

    # ===== Agent 主循环 =====
    decision = agent.think()           # Think
    result = agent.act(decision)       # Act
    agent.observe(result)              # Observe

    print("─" * 55)

    # ===== 最终报告 =====
    if result["status"] == "success":
        print()
        print("🎉 备份完成！你的日记已经安全到达 GitHub。")
        print()
        print("刚刚 Agent 做的事：")
        print("  1. Think  → 发现日记有未保存的修改")
        print("  2. Act    → git add → git commit → git push")
        print("  3. Observe → 确认推送成功")
        print()
        print("这就是 Agent 的核心模式：自己判断、自己动手、自己检查！")
    elif result["status"] == "skip":
        print()
        print("😴 没有新内容需要备份，Agent 进入休眠。")
    else:
        print()
        print("⚠️  备份遇到问题，Agent 需要人工帮助。")
        print(f"    失败详情：{result.get('msg', '未知错误')}")


if __name__ == "__main__":
    main()
