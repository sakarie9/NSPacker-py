import os
import sys
import shutil

from .utils import find_executable, run_command


def _pack_single_nca(
    nca_type: str, input_dir: str, title_id: str, output_dir: str, key_file: str
) -> str:
    """打包单个NCA文件并返回生成的NCA文件路径"""
    # 创建NCA类型对应的子目录
    nca_output_dir = os.path.join(output_dir, nca_type)
    os.makedirs(nca_output_dir, exist_ok=True)

    # 查找hacpack可执行文件
    hacpack_exe = find_executable("hacpack")

    # 构建基本命令
    command = [
        hacpack_exe,
        "-k",
        key_file,
        "-o",
        nca_output_dir,
        "--type=nca",
        f"--ncatype={nca_type}",
        f"--titleid={title_id}",
    ]

    # 根据NCA类型添加特定参数
    if nca_type == "control":
        control_dir = os.path.join(input_dir, "control/0")
        if not os.path.exists(control_dir):
            print(f"{nca_type} 目录不存在: {control_dir}")
            sys.exit(1)
        command.append(f"--romfsdir={control_dir}")
    elif nca_type == "program":
        program_exefs_dir = os.path.join(input_dir, "program/0")
        program_romfs_dir = os.path.join(input_dir, "program/1")
        program_logo_dir = os.path.join(input_dir, "program/2")

        if not os.path.exists(program_exefs_dir) or not os.path.exists(
            program_romfs_dir
        ):
            print(f"{nca_type} 目录不完整")
            sys.exit(1)

        command.extend(
            [f"--exefsdir={program_exefs_dir}", f"--romfsdir={program_romfs_dir}"]
        )

        # 如果 logo 目录存在，则添加 logodir 参数
        if os.path.exists(program_logo_dir):
            command.append(f"--logodir={program_logo_dir}")

    print(f"正在打包 {nca_type.capitalize()} NCA")
    run_command(command)

    # 找到生成的NCA文件
    nca_files = [f for f in os.listdir(nca_output_dir) if f.endswith(".nca")]
    if not nca_files:
        print(f"找不到生成的{nca_type} NCA文件")
        sys.exit(1)

    # 检查是否存在多个NCA文件的情况
    if len(nca_files) > 1:
        print(f"错误：{nca_type} NCA输出目录中存在多个NCA文件: {nca_files}")
        sys.exit(1)

    nca_name = nca_files[0]
    nca_src = os.path.join(nca_output_dir, nca_name)
    nca_dst = os.path.join(output_dir, nca_name)

    # 移动NCA到主目录
    print(f"{nca_type.capitalize()} NCA文件已生成: {nca_name}")
    os.rename(nca_src, nca_dst)

    return nca_dst


def pack_nsp(nca_dir: str, title_id: str, key_file: str):
    """将NCA文件打包成NSP文件"""
    print(f"正在打包 NSP 文件")

    # 确保输出目录存在
    os.makedirs(nca_dir, exist_ok=True)

    # 查找hacpack可执行文件
    hacpack_exe = find_executable("hacpack")

    # 构建命令
    command = [
        hacpack_exe,
        "-k",
        key_file,
        "-o",
        nca_dir,
        "--type=nsp",
        f"--titleid={title_id}",
        f"--ncadir={nca_dir}",
    ]

    run_command(command)

    print(f"NSP 文件打包完成，输出目录: {nca_dir}")


def pack_nca_files(
    input_dir: str, title_id: str, output_dir: str = "outNCA", key_file: str = "key.dat"
):
    """打包NCA文件"""
    if not os.path.exists(input_dir):
        print(f"目录不存在: {input_dir}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 使用辅助函数打包control NCA
    control_nca = _pack_single_nca("control", input_dir, title_id, output_dir, key_file)

    # 使用辅助函数打包program NCA
    program_nca = _pack_single_nca("program", input_dir, title_id, output_dir, key_file)

    # 打包 meta NCA
    print(f"正在打包 Meta NCA")

    if not os.path.exists(control_nca) or not os.path.exists(program_nca):
        print("控制或程序 NCA 文件不存在")
        sys.exit(1)

    # 查找hacpack可执行文件
    hacpack_exe = find_executable("hacpack")

    meta_command = [
        hacpack_exe,
        "-k",
        key_file,
        "-o",
        output_dir,
        "--type=nca",
        "--ncatype=meta",
        "--titletype",
        "application",
        f"--titleid={title_id}",
        f"--programnca={program_nca}",
        f"--controlnca={control_nca}",
    ]

    run_command(meta_command)

    # 清理临时目录
    try:
        control_output_dir = os.path.join(output_dir, "control")
        program_output_dir = os.path.join(output_dir, "program")
        shutil.rmtree(control_output_dir)
        shutil.rmtree(program_output_dir)
    except Exception as e:
        print(f"清理临时目录时出错: {e}")
        # 继续执行，不中断程序

    print(f"NCA 文件打包完成，输出目录: {output_dir}")
