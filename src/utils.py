import os
import subprocess
import sys
import platform
from typing import List


def find_executable(exe_name: str) -> str:
    """在PATH和当前目录中查找可执行文件，返回完整路径，支持跨平台"""
    # 准备可能的可执行文件名列表
    if platform.system() == "Windows" and not exe_name.lower().endswith(".exe"):
        exe_names = [f"{exe_name}.exe", exe_name]
    else:
        exe_names = [exe_name]

    # 检查PATH中是否存在
    from shutil import which

    for name in exe_names:
        exe_path = which(name)
        if exe_path:
            return exe_path

    # 检查当前目录
    for name in exe_names:
        current_dir_exe = os.path.join(os.getcwd(), name)
        if os.path.isfile(current_dir_exe):
            # Windows不检查执行权限
            if platform.system() == "Windows" or os.access(current_dir_exe, os.X_OK):
                return current_dir_exe

    # 都不存在，报错
    print(f"错误: 找不到可执行文件 '{exe_name}'，请确保它在PATH环境变量中或当前目录下")
    sys.exit(1)


def run_command(command: List[str]) -> str:
    """运行命令并返回输出"""
    print(f"执行命令: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {' '.join(command)}")
        print(f"错误信息: {e.stderr}")
        sys.exit(1)
