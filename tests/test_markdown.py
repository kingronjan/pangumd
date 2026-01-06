import pangu

from tests.utils import get_fixture_path

def test_code_block_rendering():
    
    filepath = get_fixture_path('codeblock.md')

    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    spaced_content = pangu.spacing_text(markdown_content)
    assert markdown_content == spaced_content
