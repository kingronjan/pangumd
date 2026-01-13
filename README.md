# pangumd



## About

This version adds special adaptations for Markdown syntax on top of the original project, ensuring that text spacing works correctly within Markdown documents.

### Current Markdown Adaptations

1. **Code Blocks** - Preserves code block formatting without adding unwanted spaces
2. **Bold Text** - Handles `**bold text**` syntax correctly, adding appropriate spacing around bold markers
3. **Italic Text** - Support for `*italic text*` syntax
4. **Chinese Links** - Proper spacing for hyperlinks containing Chinese characters

## Installation

Just clone it.

## Usage

### In Python

```python
import pangumd

new_text = pangumd.spacing_text('當你凝視著bug，bug也凝視著你')
# new_text = '當你凝視著 bug，bug 也凝視著你'

nwe_content = pangumd.spacing_file('path/to/file.txt')
# nwe_content = '與 PM 戰鬥的人，應當小心自己不要成為 PM'
```

### In CLI

```bash
$ pangumd "請使用uname -m指令來檢查你的Linux作業系統是32位元或是64位元"
請使用 uname -m 指令來檢查你的 Linux 作業系統是 32 位元或是 64 位元

$ python -m pangumd "為什麼小明有問題都不Google？因為他有Bing"
為什麼小明有問題都不 Google？因為他有 Bing

$ echo "未來的某一天，Gmail配備的AI可能會得出一個結論：想要消滅垃圾郵件最好的辦法就是消滅人類" >> path/to/file.txt
$ pangumd -f path/to/file.txt >> pangu_file.txt
$ cat pangu_file.txt
未來的某一天，Gmail 配備的 AI 可能會得出一個結論：想要消滅垃圾郵件最好的辦法就是消滅人類

$ echo "心裡想的是Microservice，手裡做的是Distributed Monolith" | pangumd
心裡想的是 Microservice，手裡做的是 Distributed Monolith

$ echo "你從什麼時候開始產生了我沒使用Monkey Patch的錯覺?" | python -m pangumd
你從什麼時候開始產生了我沒使用 Monkey Patch 的錯覺？
```

## Pre-commit Hook

To use pangumd as a pre-commit hook, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kingronjan/pangumd
    rev: 0.1.1 
    hooks:
      - id: pangumd
        files: \.(md|txt|rst)$
```

Then install the hook:

```bash
pre-commit install
```

Now pangumd will automatically run on your Markdown and text files before each commit, ensuring proper spacing between CJK and half-width characters.

## License

MIT License