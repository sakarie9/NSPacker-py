import os


def edit_npdm_title_id(directory_path, new_title_id):
    """
    编辑指定目录中的program/0/main.npdm文件，修改ProgramId字段。

    Args:
        directory_path: 包含program/0/main.npdm文件的目录路径
        new_title_id: 新的titleId，格式为16位十六进制字符串
    """
    # 构造NPDM文件路径
    npdm_path = ""
    if directory_path.endswith("main.npdm"):
        npdm_path = directory_path
    else:
        npdm_path = os.path.join(directory_path, "program", "0", "main.npdm")

    # 检查文件是否存在
    if not os.path.exists(npdm_path):
        print(f"错误：找不到文件 {npdm_path}")
        return False

    # 将title_id转换为字节
    try:
        # 确保titleId是16位十六进制字符串
        if len(new_title_id) != 16 or not all(
            c in "0123456789abcdefABCDEF" for c in new_title_id
        ):
            raise ValueError("titleId必须是16位十六进制字符串")
        title_id_bytes = int(new_title_id, 16).to_bytes(8, byteorder="little")
    except ValueError as e:
        print(f"错误：{e}")
        return False

    # 读取NPDM文件
    with open(npdm_path, "rb") as f:
        npdm_data = bytearray(f.read())

    # 查找ACI0魔术值
    aci0_magic = b"ACI0"
    aci0_pos = npdm_data.find(aci0_magic)

    if aci0_pos == -1:
        print(f"错误：在NPDM文件中找不到ACI0段")
        return False

    # 在ACI0中，ProgramId在偏移量0x10处
    program_id_offset = aci0_pos + 0x10

    # 保存原始ProgramId以供显示
    original_title_id = int.from_bytes(
        npdm_data[program_id_offset : program_id_offset + 8], byteorder="little"
    )
    original_title_id_hex = format(original_title_id, "016x")

    # 写入新的ProgramId
    npdm_data[program_id_offset : program_id_offset + 8] = title_id_bytes

    # 写回文件
    with open(npdm_path, "wb") as f:
        f.write(npdm_data)

    print(
        f"成功：已将 {npdm_path} 的ProgramId从 {original_title_id_hex} 修改为 {new_title_id}"
    )
    return True


def edit_nacp_file(directory_path, title_id, name=None, author=None, version=None):
    """
    编辑指定目录中的control/0/control.nacp文件，修改游戏名称、作者、版本和titleId相关字段。

    Args:
        directory_path: 包含control/0/control.nacp文件的目录路径或直接的文件路径
        title_id: 标题ID，格式为16位十六进制字符串
        name: 游戏名称，可选，为None或空字符串时跳过修改
        author: 游戏作者，可选，为None或空字符串时跳过修改
        version: 显示版本，可选，为None或空字符串时跳过修改
    """
    # 构造NACP文件路径
    nacp_path = ""
    if directory_path.endswith("control.nacp"):
        nacp_path = directory_path
    else:
        nacp_path = os.path.join(directory_path, "control", "0", "control.nacp")

    # 检查文件是否存在
    if not os.path.exists(nacp_path):
        print(f"错误：找不到文件 {nacp_path}")
        return False

    # 将title_id转换为字节
    try:
        # 确保titleId是16位十六进制字符串
        if len(title_id) != 16 or not all(
            c in "0123456789abcdefABCDEF" for c in title_id
        ):
            raise ValueError("titleId必须是16位十六进制字符串")
        title_id_int = int(title_id, 16)
        title_id_bytes = title_id_int.to_bytes(8, byteorder="little")
    except ValueError as e:
        print(f"错误：{e}")
        return False

    # 读取NACP文件
    with open(nacp_path, "rb") as f:
        nacp_data = bytearray(f.read())

    # 1. 对每个不为空的NacpLanguageEntry，修改name和author（如果提供）
    if name or author:
        lang_entries_count = 16
        name_size = 0x200
        author_size = 0x100
        lang_entry_size = name_size + author_size

        for i in range(lang_entries_count):
            # 计算当前NacpLanguageEntry的偏移量
            lang_entry_offset = i * lang_entry_size
            name_offset = lang_entry_offset
            author_offset = lang_entry_offset + name_size

            # 检查name字段是否为空 (检查第一个字节是否为0)
            if nacp_data[name_offset] != 0:
                # 修改name字段（如果提供）
                if name:
                    name_bytes = name.encode("utf-8")
                    name_bytes = name_bytes[: name_size - 1]  # 留出一个字节给null终止符
                    # 清空原有内容
                    for j in range(name_size):
                        nacp_data[name_offset + j] = 0
                    # 写入新内容
                    nacp_data[name_offset : name_offset + len(name_bytes)] = name_bytes

                # 修改author字段（如果提供）
                if author:
                    author_bytes = author.encode("utf-8")
                    author_bytes = author_bytes[
                        : author_size - 1
                    ]  # 留出一个字节给null终止符
                    # 清空原有内容
                    for j in range(author_size):
                        nacp_data[author_offset + j] = 0
                    # 写入新内容
                    nacp_data[author_offset : author_offset + len(author_bytes)] = (
                        author_bytes
                    )

    # 2. 修改display_version字段（如果提供）
    if version:
        display_version_offset = 0x3060
        display_version_size = 0x10

        version_bytes = version.encode("utf-8")
        version_bytes = version_bytes[
            : display_version_size - 1
        ]  # 留出一个字节给null终止符
        # 清空原有内容
        for i in range(display_version_size):
            nacp_data[display_version_offset + i] = 0
        # 写入新内容
        nacp_data[
            display_version_offset : display_version_offset + len(version_bytes)
        ] = version_bytes

    # 3. 修改local_communication_id字段 (8个u64，每个8字节)
    local_comm_id_offset = 0x30B0

    for i in range(8):
        offset = local_comm_id_offset + i * 8
        nacp_data[offset : offset + 8] = title_id_bytes

    # 4. 修改pseudo_device_id_seed字段 (u64, 8字节)
    pseudo_device_id_offset = 0x30F8
    nacp_data[pseudo_device_id_offset : pseudo_device_id_offset + 8] = title_id_bytes

    # 写回文件
    with open(nacp_path, "wb") as f:
        f.write(nacp_data)

    # 打印成功信息
    print(f"成功：已修改 {nacp_path} 的游戏信息")
    if name:
        print(f"  - 游戏名称：{name}")
    if author:
        print(f"  - 作者：{author}")
    if version:
        print(f"  - 版本：{version}")
    print(f"  - 标题ID：{title_id}")
    return True
