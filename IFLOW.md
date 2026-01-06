# IFLOW.md - pangu.py 项目上下文

## 项目概述

**pangu.py** 是一个用于改善中文、日文、韩文（CJK）与半角字符（字母、数字、符号）之间可读性的文本间距处理工具。它自动在 CJK 字符和半角字符之间插入空格，提升文本的可读性。

### 核心特性

- **Paranoid Text Spacing 算法**：实现了 v4 版本的偏执文本间距算法
- **多语言支持**：支持中文（简体/繁体）、日文、韩文
- **多种使用方式**：
  - Python 模块导入使用
  - 命令行工具（CLI）
  - 文件处理
- **Python 版本**：支持 Python 3.3+（当前要求 Python >= 3.13）

### 项目结构

```
pangu.py/
├── pangu.py              # 主程序文件，包含核心算法和 CLI
├── tests/                # 测试目录
│   ├── test_pangu.py     # 主要测试文件
│   ├── test_markdown.py  # Markdown 相关测试
│   └── fixtures/         # 测试数据
├── pyproject.toml        # 现代 Python 项目配置（使用 uv）
├── setup.py              # 传统 setuptools 配置
├── Makefile              # 构建和发布脚本
└── README.rst            # 项目文档
```

## 构建和运行

### 环境要求

- Python >= 3.13
- uv（推荐）或 pip

### 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用传统 pip
pip install -e .
```

### 运行测试

```bash
# 使用 uv 运行测试（推荐）
uv run -m pytest tests/ -v

# 或使用 Makefile
make test

# 或直接使用 pytest
pytest tests/ -v
```

### 使用方式

#### Python 模块使用

```python
import pangu

# 处理文本
new_text = pangu.spacing_text('當你凝視著bug，bug也凝視著你')
# 输出: '當你凝視著 bug，bug 也凝視著你'

# 处理文件
content = pangu.spacing_file('path/to/file.txt')
```

#### 命令行使用

```bash
# 处理文本字符串
pangu "請使用uname -m指令來檢查你的Linux作業系統"

# 处理文件
pangu -f path/to/file.txt

# 使用管道
echo "心裡想的是Microservice" | pangu

# 作为模块运行
python -m pangu "為什麼小明有問題都不Google？"
```

### 构建和发布

```bash
# 清理构建文件
make clean

# 打包
make pack

# 发布到 PyPI
make publish
```

## 开发约定

### 代码风格

- 使用 UTF-8 编码
- 遵循 Python PEP 8 规范
- 使用正则表达式进行文本处理
- 主程序文件为单文件模块（pangu.py）

### 测试约定

- 使用 pytest 作为测试框架
- 测试文件位于 `tests/` 目录
- 测试函数命名以 `test_` 开头
- 测试使用断言进行验证
- 包含 57 个测试用例，覆盖各种字符组合和边界情况

### 核心算法说明

项目使用多个正则表达式来处理不同的字符组合：

1. **CJK 与字母/数字的间距**：在 CJK 字符和半角字符之间添加空格
2. **标点符号转换**：将某些标点符号转换为全角符号
3. **引号处理**：处理引号与 CJK 字符之间的间距
4. **特殊符号处理**：处理运算符、括号等特殊符号

**重要修复**：`FIX_QUOTE_ANY_QUOTE` 正则表达式已修复，现在只匹配单个引号，避免错误匹配 markdown 代码块（三个或更多连续反引号）。

### 版本管理

- 版本号定义在 `pangu.py` 中的 `__version__` 变量
- 当前版本：4.0.6.1
- 使用语义化版本控制

### CI/CD

- 使用 Travis CI 进行持续集成
- 测试覆盖 Python 3.3-3.7
- 使用 codecov 进行代码覆盖率统计

## 常见任务

### 添加新测试

在 `tests/` 目录下添加新的测试文件或扩展现有测试文件。测试应该遵循现有的命名约定和结构。

### 修改核心算法

核心算法位于 `pangu.py` 的 `spacing()` 函数中。修改后务必运行完整的测试套件确保没有破坏现有功能。

### 发布新版本

1. 更新 `pangu.py` 中的 `__version__`
2. 更新 `HISTORY.rst` 添加版本说明
3. 运行 `make pack` 构建包
4. 运行 `make publish` 发布到 PyPI

## 注意事项

- 项目不支持 Python 2.7（已在 4.0.6.1 版本移除）
- 正则表达式处理需要特别注意边界情况，特别是 markdown 代码块
- 测试覆盖率要求高，任何修改都应该通过所有现有测试
- 使用 uv 进行依赖管理时，确保 `.venv` 目录被正确忽略