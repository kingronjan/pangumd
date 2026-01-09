import argparse
import os

import pangu

__version__ = '0.1.6'
__all__ = ['spacing', 'spacing_file', 'cli']


def spacing(text):
    """
    使用 mistune 解析 markdown 文本内容，参考文档：https://mistune.lepture.com/en/latest/renderers.html
    并调用 pangu 库对文本进行间距处理，以下内容除外：

        - 代码块（Code Block）
        - 行内代码（Inline Code）
        - 链接（Link）的 url 部分
        - 图片（Image）的 url 部分
        - 粗体（Bold）
        - 斜体（Italic）
        - 删除线（Strikethrough）

    注意，粗体、斜体、删除线等内容周围如果包含 CJK 字符，则会被间距处理，比如：

        "this is**示例**over." -> "this is **示例** over."

    处理完成后使用 mistune.renderers.markdown.MarkdownRenderer 将解析树重新渲染为 markdown 文本并返回。
    """
    return pangu.spacing(text)


def spacing_file(path):
    """
    Perform paranoid text spacing on file content.
    Automatically detects markdown files and uses mistletoe parser if available.
    
    Args:
        path: The file path to read and process
        
    Returns:
        The processed file content with proper spacing
    """
    with open(os.path.abspath(path), encoding='utf-8') as f:
        content = f.read()
        return spacing(content)


def cli():
    parser = argparse.ArgumentParser(
        description='Paranoid text spacing for good readability, to automatically insert whitespace between CJK (Chinese, Japanese, Korean) and half-width characters (alphabetical letters, numerical digits and symbols).'
    )
    parser.add_argument('files', nargs='+', help='Files to be processed')
    args = parser.parse_args()

    for filepath in args.files:
        content = spacing_file(filepath)
        with open(filepath, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    cli()
