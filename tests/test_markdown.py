from textwrap import dedent

import pangumd


def test_strong_emphasis():
    assert pangumd.spacing_text('Hello**你好**吗') == 'Hello **你好**吗'
    assert pangumd.spacing_text('今天的天气**很不错**哦') == '今天的天气**很不错**哦'
    assert pangumd.spacing_text('这是\n**bold**字体') == '这是\n**bold** 字体'
    assert pangumd.spacing_text('这是**bold**,字体') == '这是 **bold**, 字体'
    assert pangumd.spacing_text('这是**bo*加*ld**,字体') == '这是 **bo *加* ld**, 字体'


def test_function_call_not_modified():
    assert (
        pangumd.spacing_text('用`function_call(param1, param2)`函数')
        == '用 `function_call(param1, param2)`函数'
    )
    assert (
        pangumd.spacing_text('用`function_call(param1): return`函数')
        == '用 `function_call(param1): return` 函数'
    )


def test_indent_after_blank_line():
    text = dedent("""
    据我所知目前的几种规范落地工具：

    - [openspec](https://github.com/Fission-AI/OpenSpec)
    - [github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development](https://github.com/github/spec-kit)

    我目前仅仅使用过 openspec。""")
    assert pangumd.spacing_text(text) == text


# def test_all():
#     filepath = get_fixture_path('all.md')
#     fix_filepath = get_fixture_path('all_fixed.md')

#     with open(filepath, "r", encoding="utf-8") as f:
#         markdown_content = f.read()

#     with open(fix_filepath, "r", encoding="utf-8") as f:
#         fixed_content = f.read()

#     spaced_content = pangumd.spacing(markdown_content)
#     assert spaced_content == fixed_content
