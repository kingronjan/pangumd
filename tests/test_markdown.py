import pangu

from tests.utils import get_fixture_path

def test_code_block_rendering():
    
    filepath = get_fixture_path('codeblock.md')

    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    spaced_content = pangu.spacing_text(markdown_content)
    assert markdown_content == spaced_content


def test_bold_font():
    assert pangu.spacing_text("Hello**你好**吗") == "Hello **你好**吗"
    assert pangu.spacing_text("今天的天气**很不错**哦") == "今天的天气 **很不错** 哦"
