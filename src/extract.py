import os
import re
import sys
from typing import Dict, List

from .utils import find_executable, run_command


def extract_nca_info(hactool_output: str) -> List[Dict[str, str]]:
    """从hactoolnet输出中提取NCA信息"""
    nca_info_list = []
    nca_section = False

    for line in hactool_output.split("\n"):
        # 找到NCA信息部分的开始
        if "NCA ID" in line and "Type" in line and "Title ID" in line:
            nca_section = True
            continue

        if nca_section and line.strip():
            # 使用正则表达式匹配NCA ID, Type和Title ID
            match = re.match(r"(\w{32})\s+(\w+)\s+(\w{16})", line.strip())
            if match:
                nca_id, nca_type, title_id = match.groups()
                nca_info_list.append(
                    {"nca_id": nca_id, "type": nca_type, "title_id": title_id}
                )

    return nca_info_list


def process_nsp_file(nsp_path: str, output_dir: str = "out-nsp"):
    """处理NSP文件，解析和解包NCA文件"""
    if not os.path.exists(nsp_path):
        print(f"文件不存在: {nsp_path}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 1. 使用hactoolnet获取NCA信息
    hactoolnet_exe = find_executable("hactoolnet")
    print(f"正在解析NSP文件: {nsp_path}")
    command = [hactoolnet_exe, "-t", "pfs0", nsp_path, "--listncas"]
    output = run_command(command)
    print(output)

    # 2. 提取NCA信息
    nca_info_list = extract_nca_info(output)
    if not nca_info_list:
        print("无法提取NCA信息")
        sys.exit(1)

    # 获取title_id (假设所有NCA的title_id相同)
    title_id = nca_info_list[0]["title_id"]

    # 3. 使用nstool解包NSP文件
    nstool_exe = find_executable("nstool")
    print(f"正在解包NSP文件到: {output_dir}")
    nstool_command = [nstool_exe, "-x", output_dir, nsp_path]
    run_command(nstool_command)

    # 4. 根据类型解包对应的NCA文件
    nca_files = {}
    for nca_info in nca_info_list:
        nca_id = nca_info["nca_id"]
        nca_type = nca_info["type"].lower()
        nca_file = f"{nca_id}.nca"
        nca_files[nca_type] = nca_file

    # 获取当前工作目录中的NCA文件
    try:
        # 更改工作目录到输出目录
        original_dir = os.getcwd()
        os.chdir(output_dir)

        # 解包Control NCA
        if "control" in nca_files:
            control_nca = nca_files["control"]
            print(f"正在解包Control NCA: {control_nca}")
            nstool_control_command = [nstool_exe, "-x", "control", control_nca]
            run_command(nstool_control_command)

        # 解包Program NCA
        if "program" in nca_files:
            program_nca = nca_files["program"]
            print(f"正在解包Program NCA: {program_nca}")
            nstool_program_command = [nstool_exe, "-x", "program", program_nca]
            run_command(nstool_program_command)

        # 恢复原始工作目录
        os.chdir(original_dir)
    except Exception as e:
        print(f"解包NCA文件时发生错误: {e}")
        # 确保恢复原始工作目录
        os.chdir(original_dir)
        sys.exit(1)

    print(f"NSP文件处理完成: {nsp_path}")
