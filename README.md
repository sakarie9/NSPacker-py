# NSPacker-py

[English](./README_EN.md) | 中文

NSPacker-py 是一个用于处理任天堂Switch游戏包文件(NSP)的命令行工具。该工具可以解包、编辑和重新打包NSP文件。

## 功能

- **解包NSP文件**：解包NSP文件
- **编辑NSP信息**：修改游戏的标题ID、名称、作者和版本信息
- **打包NCA文件**：将编辑后的内容重新打包为NSP文件

## 安装

```bash
git clone https://github.com/yourusername/nspacker-py.git
cd nspacker-py
```

## 使用方法

### 二进制获取

本脚本调用了外部二进制文件以简化代码

使用前需要将所需的文件放在 `main.py` 同级目录下，或者放在 `PATH` 环境变量中

> [!IMPORTANT]
> 缺少 `nstool` 及 `hactoolnet` 会导致无法解包

> [!IMPORTANT]
>缺少 `hacpack` 会导致无法封包

- [jakcron/nstool](https://github.com/jakcron/nstool)
- [Thealexbarney/LibHac](https://github.com/Thealexbarney/LibHac)
   下载 `hactoolnet`
- hacpack
   `hacpack` 原仓库已删除，须从 fork 仓库中自行编译。Linux 用户可尝试使用本仓库预编译的 `hacpack`, Windows 用户请自行编译

```plain
示例目录结构：
.
├── hacpack
├── hactoolnet
├── main.py
└── nstool
```

### 解包NSP文件

```bash
python main.py extract <nsp文件路径> [-o 输出目录]
```

选项：

- `-o, --output`: 指定输出目录，默认为"out-nsp"

示例：

```bash
python main.py extract /path/to/game.nsp -o extracted_game
```

### 编辑NSP信息

```bash
python main.py edit <目录路径> [-t TitleID] [-n 游戏名称] [-a 作者] [-v 版本]
```

选项：

- `-t, --title_id`: 新的TitleID（例如: 0100000000010000）
- `-n, --name`: 游戏名称
- `-a, --author`: 游戏作者
- `-v, --version`: 显示版本

示例：

```bash
python main.py edit extracted_game -t 0100000000010000 -n "My Game" -a "Me" -v "1.0.0"
```

### 打包NCA文件

```bash
python main.py pack <输入目录> -t <标题ID> [-o 输出目录] [-k 密钥文件路径]
```

选项：

- `-t, --titleid`: TitleID（例如: 0100000000010000）
- `-o, --output`: 指定输出目录，默认为"outNCA"
- `-k, --key`: 密钥文件路径，默认为"key.dat"

示例：

```bash
python main.py pack extracted_game -t 0100000000010000 -o packaged_game
```

## 注意事项

- 使用此工具前请确保您拥有对相关游戏内容的合法权利
- 在编辑NSP文件时，请确保title_id格式正确（16位十六进制字符串）
- 打包前需要准备有效的密钥文件

## 许可证注意事项

本仓库中包含或使用的第三方工具受其各自许可证约束：

- **nstool**: 请参考 [jakcron/nstool](https://github.com/jakcron/nstool) 的许可证
- **hactoolnet**: 请参考 [Thealexbarney/LibHac](https://github.com/Thealexbarney/LibHac) 的许可证
- **hacpack**: 原始许可证适用，如使用本仓库预编译版本，使用风险自负

如需重分发这些工具，请确保遵守它们各自的许可条款。
