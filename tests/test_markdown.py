from textwrap import dedent

import pangumd
from tests.utils import get_fixture_path


def test_code_block_newline_kept():
    
    filepath = get_fixture_path('codeblock.md')

    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    spaced_content = pangumd.spacing(markdown_content)
    assert markdown_content == spaced_content


def test_json_code_block_not_modified():
    text = dedent("""
    2. 配置连接器，连接器可以使用如下配置

        ```json
        {
            "name": "inventory-connector",
            "config": {
                "database.user": "${file:/secrets/mysql.properties:user}",
                "database.password": "${file:/secrets/mysql.properties:password}",
                ...
            }
        }
        ```
    """)
    assert pangumd.spacing(text) == text


def test_bold_font():
    assert pangumd.spacing("Hello**你好**吗") == "Hello **你好**吗"
    assert pangumd.spacing("今天的天气**很不错**哦") == "今天的天气**很不错**哦"

def test_command_args_not_formatted():
    text = dedent("""
    ```bash
    RUN sed -i 's/apt.p/apt-archive.p/g' /etc/apt/sources.list.d/pgdg.list
    ```
    """)
    assert pangumd.spacing(text) == text


def test_function_call_not_modified():
    text = dedent("""
    请使用 `function_call(param1, param2)` 来调用函数。
    """)
    assert pangumd.spacing(text) == text


def test_multipleline_content():
    content='## 相关项目\n- [pydantic/pydantic-settings: Settings management using pydantic](https://github.com/pydantic/pydantic-settings) 使用 pydantic 作为 settings 配置（以python 类的形式），可以按优先级从 `.env`，env，命令行参数中获取配置值，并将配置值转换指定的数据格式\n'

    assert pangumd.spacing(content) == '## 相关项目\n- [pydantic/pydantic-settings: Settings management using pydantic](https://github.com/pydantic/pydantic-settings) 使用 pydantic 作为 settings 配置（以 python 类的形式），可以按优先级从 `.env`，env，命令行参数中获取配置值，并将配置值转换指定的数据格式\n'


def test_all():
    filepath = get_fixture_path('all.md')
    fix_filepath = get_fixture_path('all_fixed.md')

    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(fix_filepath, "r", encoding="utf-8") as f:
        fixed_content = f.read()
    
    spaced_content = pangumd.spacing(markdown_content)
    assert spaced_content == fixed_content
