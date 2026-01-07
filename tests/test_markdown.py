from textwrap import dedent

import pangumd
from tests.utils import get_fixture_path


def test_code_block_newline_kept():
    
    filepath = get_fixture_path('codeblock.md')

    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    spaced_content = pangumd.spacing_text(markdown_content)
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
    assert pangumd.spacing_text(text) == text


def test_bold_font():
    assert pangumd.spacing_text("Hello**你好**吗") == "Hello **你好**吗"
    assert pangumd.spacing_text("今天的天气**很不错**哦") == "今天的天气 **很不错** 哦"
    
    text = dedent("""
    * **column**

        * 描述：目的表需要写入数据的字段,字段之间用英文逗号分隔。例如: "column": ["id","name","age"]。如果要依次写入全部列，使用 `*` 表示，例如:`"column": ["*"]`。

                **column配置项必须指定，不能留空！**
    """)
    assert pangumd.spacing_text(text) == text


def test_command_args_not_formatted():
    text = dedent("""
    ```bash
    RUN sed -i 's/apt.p/apt-archive.p/g' /etc/apt/sources.list.d/pgdg.list
    ```
    """)
    assert pangumd.spacing_text(text) == text


def test_function_call_not_modified():
    text = dedent("""
    请使用 `function_call(param1, param2)` 来调用函数。
    """)
    assert pangumd.spacing_text(text) == text
