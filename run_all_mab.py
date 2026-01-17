"""
一次性并行运行三种 MAB 算法的小助手脚本。

作用：
- 启动三个子进程，分别运行：
  - mab_train_lr.py --algo eps
  - mab_train_lr.py --algo ucb
  - mab_train_lr.py --algo ts
- 三个进程并行运行，互不影响。
- 所有结果仍然保存在 runs/mab_lr/ 下。

使用方式（在项目根目录）：

    python run_all_mab.py

运行完成后，如果你想生成三条曲线的对比图，再执行：

    python mab_train_lr.py --algo compare
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    # 你可以在这里修改默认参数
    python_exe = sys.executable  # 当前解释器
    script = "mab_train_lr.py"

    # 公共参数（如需修改 data / epochs / rounds，可改这里）
    common_args = [
        "--data",
        "mymodel4.yaml",
        "--epochs",
        "5",
        "--rounds",
        "100",
        # 设备设置：如果系统有 GPU，可以指定 "--device 0"
        # 如果没有 GPU 或想自动检测，可以移除下面两行，让程序自动检测
        # "--device",
        # "0",
    ]

    # 为了防止相对路径问题，确保在脚本所在目录运行
    root = Path(__file__).resolve().parent
    script_path = root / script

    if not script_path.exists():
        print(f"[run_all_mab] 错误：未找到脚本 {script_path}")
        return

    commands = [
        [python_exe, str(script_path), "--algo", "etc", *common_args],
        [python_exe, str(script_path), "--algo", "ucb", *common_args],
        [python_exe, str(script_path), "--algo", "ts", *common_args],
    ]

    print("[run_all_mab] 将并行启动以下三个命令：")
    for cmd in commands:
        print("  ", " ".join(cmd))

    processes = []
    for cmd in commands:
        # creationflags 在 Windows 上避免弹出多个控制台窗口（可选）
        try:
            p = subprocess.Popen(cmd, cwd=root)
        except Exception as e:
            print(f"[run_all_mab] 启动进程失败: {cmd} | 错误: {e}")
            continue
        processes.append(p)

    print("[run_all_mab] 已启动全部子进程，正在等待它们结束...")

    for i, p in enumerate(processes, start=1):
        ret = p.wait()
        print(f"[run_all_mab] 子进程 {i} 退出码: {ret}")

    print(
        "\n[run_all_mab] 所有算法已运行完成。\n"
        "如果需要生成三条曲线的对比图，请再执行：\n"
        "    python mab_train_lr.py --algo compare\n"
    )


if __name__ == "__main__":
    main()

