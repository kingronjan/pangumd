#!/usr/bin/env python
# coding: utf-8
"""
Paranoid text spacing for good readability, to automatically insert whitespace between CJK (Chinese, Japanese, Korean) and half-width characters (alphabetical letters, numerical digits and symbols).

>>> import pangumd
>>> nwe_text = pangumd.spacing_text('當你凝視著bug，bug也凝視著你')
>>> print(nwe_text)
'當你凝視著 bug，bug 也凝視著你'
>>> nwe_content = pangumd.spacing_file('path/to/file.txt')
>>> print(nwe_content)
'與 PM 戰鬥的人，應當小心自己不要成為 PM'
"""

import argparse
import os
import re
import sys

try:
    from mistletoe import Document
    from mistletoe.ast_renderer import ASTRenderer
    MISTLETOE_AVAILABLE = True
except ImportError:
    MISTLETOE_AVAILABLE = False

__version__ = '0.1.6'
__all__ = ['spacing_text', 'spacing_file', 'spacing', 'cli']

CJK = r'\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30fa\u30fc-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'

ANY_CJK = re.compile(r'[{CJK}]'.format(CJK=CJK))

CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK = re.compile('([{CJK}])([ ]*(?:[\\:]+|\\.)[ ]*)([{CJK}])'.format(CJK=CJK))  # there is an extra non-capturing group compared to JavaScript version
CONVERT_TO_FULLWIDTH_CJK_SYMBOLS = re.compile('([{CJK}])[ ]*([~\\!;,\\?]+)[ ]*'.format(CJK=CJK))
DOTS_CJK = re.compile('([\\.]{{2,}}|\u2026)([{CJK}])'.format(CJK=CJK))  # need to escape { }
FIX_CJK_COLON_ANS = re.compile('([{CJK}])\\:([A-Z0-9\\(\\)])'.format(CJK=CJK))

CJK_QUOTE = re.compile('([{CJK}])([`"\u05f4])'.format(CJK=CJK))  # no need to escape `
QUOTE_CJK = re.compile('([`"\u05f4])([{CJK}])'.format(CJK=CJK))  # no need to escape `
FIX_QUOTE_ANY_QUOTE = re.compile(r'(?<!`)([`"\u05f4])(\s*)(.+?)(\s*)([`"\u05f4])(?!`)')

CJK_SINGLE_QUOTE_BUT_POSSESSIVE = re.compile("([{CJK}])('[^s])".format(CJK=CJK))
SINGLE_QUOTE_CJK = re.compile("(')([{CJK}])".format(CJK=CJK))
FIX_POSSESSIVE_SINGLE_QUOTE = re.compile("([{CJK}A-Za-z0-9])( )('s)".format(CJK=CJK))

HASH_ANS_CJK_HASH = re.compile('([{CJK}])(#)([{CJK}]+)(#)([{CJK}])'.format(CJK=CJK))
CJK_HASH = re.compile('([{CJK}])(#([^ ]))'.format(CJK=CJK))
HASH_CJK = re.compile('(([^ ])#)([{CJK}])'.format(CJK=CJK))

CJK_OPERATOR_ANS = re.compile('([{CJK}])([\\+\\-\\*\\/=&\\|<>])([A-Za-z0-9])'.format(CJK=CJK))
ANS_OPERATOR_CJK = re.compile('([A-Za-z0-9])([\\+\\-\\*\\/=&\\|<>])([{CJK}])'.format(CJK=CJK))

FIX_SLASH_AS = re.compile(r'([/]) ([a-z\-_\./]+)')
FIX_SLASH_AS_SLASH = re.compile(r'([/\.])([A-Za-z\-_\./]+) ([/])')

CJK_LEFT_BRACKET = re.compile('([{CJK}])([\\(\\[\\{{<>\u201c])'.format(CJK=CJK))  # need to escape {
RIGHT_BRACKET_CJK = re.compile('([\\)\\]\\}}<>\u201d])([{CJK}])'.format(CJK=CJK))  # need to escape }
FIX_LEFT_BRACKET_ANY_RIGHT_BRACKET = re.compile(r'([\(\[\{<\u201c]+)(\s*)(.+?)(\s*)([\)\]\}>\u201d]+)')  # need to escape { }
ANS_CJK_LEFT_BRACKET_ANY_RIGHT_BRACKET = re.compile('([A-Za-z0-9{CJK}])[ ]*([\u201c])([A-Za-z0-9{CJK}\\-_ ]+)([\u201d])'.format(CJK=CJK))
LEFT_BRACKET_ANY_RIGHT_BRACKET_ANS_CJK = re.compile('([\u201c])([A-Za-z0-9{CJK}\\-_ ]+)([\u201d])[ ]*([A-Za-z0-9{CJK}])'.format(CJK=CJK))

AN_LEFT_BRACKET = re.compile(r'([A-Za-z0-9])([\(\[\{])')
RIGHT_BRACKET_AN = re.compile(r'([\)\]\}])([A-Za-z0-9])')

CJK_ANS = re.compile('([{CJK}])([A-Za-z\u0370-\u03ff0-9@\\$%\\^&\\*\\-\\+\\\\=\\|/\u00a1-\u00ff\u2150-\u218f\u2700—\u27bf])'.format(CJK=CJK))
ANS_CJK = re.compile('([A-Za-z\u0370-\u03ff0-9~\\!\\$%\\^&\\*\\-\\+\\\\=\\|;:,\\./\\?\u00a1-\u00ff\u2150-\u218f\u2700—\u27bf])([{CJK}])'.format(CJK=CJK))

S_A = re.compile(r'(%)([A-Za-z])')

MIDDLE_DOT = re.compile(r'([ ]*)([\u00b7\u2022\u2027])([ ]*)')

# Python version only
TILDES = re.compile(r'~+')
EXCLAMATION_MARKS = re.compile(r'!+')
SEMICOLONS = re.compile(r';+')
COLONS = re.compile(r':+')
COMMAS = re.compile(r',+')
PERIODS = re.compile(r'\.+')
QUESTION_MARKS = re.compile(r'\?+')


def convert_to_fullwidth(symbols):
    symbols = TILDES.sub('～', symbols)
    symbols = EXCLAMATION_MARKS.sub('！', symbols)
    symbols = SEMICOLONS.sub('；', symbols)
    symbols = COLONS.sub('：', symbols)
    symbols = COMMAS.sub('，', symbols)
    symbols = PERIODS.sub('。', symbols)
    symbols = QUESTION_MARKS.sub('？', symbols)
    return symbols.strip()


def _protect_markdown_syntax(text):
    """
    Protect markdown code blocks, markdown links, URL anchors, bold and italic syntax by replacing them with placeholders.
    Returns a tuple of (protected_text, patterns_list).
    """
    markdown_patterns = []
    def protect_markdown(match):
        markdown_patterns.append(match.group(0))
        return f'\x00MARKDOWN{len(markdown_patterns) - 1}\x00'
    
    # Protect code blocks first (before inline code, bold/italic)
    # Match ```code```
    protected_text = re.sub(r'```[\s\S]*?```', protect_markdown, text)
    
    # Protect markdown links (before inline code, bold/italic)
    # Match [text](url)
    protected_text = re.sub(r'\[[^\]]+\]\([^\)]+\)', protect_markdown, protected_text)
    
    # Protect URL anchors (before inline code, bold/italic)
    # Match https://...#CJK or http://...#CJK
    protected_text = re.sub(r'https?://[^\s)]+#[{CJK}]+'.format(CJK=CJK), protect_markdown, protected_text)
    
    # Protect inline code patterns (before bold/italic)
    # Match `code` but not ```code``` (code blocks)
    protected_text = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', protect_markdown, protected_text)
    
    # Protect **text** patterns (but not inside backticks)
    protected_text = re.sub(r'(?<!`)(\*\*)([^*`]+?)(\*\*)(?!`)', protect_markdown, protected_text)
    # Protect *text* patterns (but not **text** and not inside backticks)
    # Use word boundaries to ensure we don't match parts of **text**
    protected_text = re.sub(r'(?<!`)(?<!\*)(\*)(?!\*)([^*\n`]+?)(?<!\*)(\*)(?!\*)(?!`)', protect_markdown, protected_text)
    
    return protected_text, markdown_patterns


def _restore_markdown_syntax(text, markdown_patterns):
    """
    Restore markdown patterns from placeholders with intelligent spacing.
    """
    for i, pattern in enumerate(markdown_patterns):
        placeholder = f'\x00MARKDOWN{i}\x00'
        if placeholder not in text:
            continue
        
        # Find the context around the placeholder
        idx = text.find(placeholder)
        prev_char = text[idx - 1] if idx > 0 else ''
        next_char = text[idx + len(placeholder)] if idx + len(placeholder) < len(text) else ''
        
        # Extract the content inside the markdown syntax (without the ** or * markers)
        # For **text**, extract "text"
        content = pattern
        if pattern.startswith('**') and pattern.endswith('**'):
            content = pattern[2:-2]
        elif pattern.startswith('*') and pattern.endswith('*'):
            content = pattern[1:-1]
        
        # Determine if the content contains CJK
        has_cjk = bool(ANY_CJK.search(content))
        
        # Determine if we need spaces
        # Different rules for different markdown syntax:
        # - For backticks (inline code): Add space with CJK and ANS
        # - For **/* (bold/italic): Add space only with ANS, NOT with CJK
        needs_space_before = False
        needs_space_after = False
        
        is_backtick = pattern.startswith('`') and pattern.endswith('`')
        
        if prev_char:
            if is_backtick:
                # For backticks, add space with CJK and ANS
                if bool(ANY_CJK.match(prev_char)) or prev_char.isalnum() or prev_char in '.,;:!?()[]{}"\'':
                    needs_space_before = True
            else:
                # For **/*, add space only with ANS, NOT with CJK
                if bool(ANY_CJK.match(prev_char)):
                    needs_space_before = False
                elif prev_char.isalnum() or prev_char in '.,;:!?()[]{}"\'':
                    needs_space_before = True
        
        if next_char:
            if is_backtick:
                # For backticks, add space with CJK and ANS
                if bool(ANY_CJK.match(next_char)) or next_char.isalnum() or next_char in '.,;:!?()[]{}"\'':
                    needs_space_after = True
            else:
                # For **/*, add space only with ANS, NOT with CJK
                if bool(ANY_CJK.match(next_char)):
                    needs_space_after = False
                elif next_char.isalnum() or next_char in '.,;:!?()[]{}"\'':
                    needs_space_after = True
        
        # Build replacement
        replacement = pattern
        if needs_space_before and prev_char != ' ':
            replacement = ' ' + replacement
        if needs_space_after and next_char != ' ':
            replacement = replacement + ' '
        
        text = text.replace(placeholder, replacement, 1)
    
    return text


def spacing(text):
    """
    Perform paranoid text spacing on text.
    """
    if len(text) <= 1 or not ANY_CJK.search(text):
        return text

    new_text = text

    # Protect markdown bold and italic syntax FIRST
    new_text, markdown_patterns = _protect_markdown_syntax(new_text)

    # TODO: refactoring
    matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK.search(new_text)
    while matched:
        start, end = matched.span()
        new_text = ''.join((new_text[:start + 1], convert_to_fullwidth(new_text[start + 1:end - 1]), new_text[end - 1:]))
        matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS_CJK.search(new_text)

    matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS.search(new_text)
    while matched:
        start, end = matched.span()
        new_text = ''.join((new_text[:start + 1], convert_to_fullwidth(new_text[start + 1:end]), new_text[end:]))
        matched = CONVERT_TO_FULLWIDTH_CJK_SYMBOLS.search(new_text)

    new_text = DOTS_CJK.sub(r'\1 \2', new_text)
    new_text = FIX_CJK_COLON_ANS.sub(r'\1：\2', new_text)

    new_text = CJK_QUOTE.sub(r'\1 \2', new_text)
    new_text = QUOTE_CJK.sub(r'\1 \2', new_text)
    new_text = FIX_QUOTE_ANY_QUOTE.sub(r'\1\3\5', new_text)  # error for code like ``` `` ` ```

    new_text = CJK_SINGLE_QUOTE_BUT_POSSESSIVE.sub(r'\1 \2', new_text)
    new_text = SINGLE_QUOTE_CJK.sub(r'\1 \2', new_text)
    new_text = FIX_POSSESSIVE_SINGLE_QUOTE.sub(r"\1's", new_text)

    new_text = HASH_ANS_CJK_HASH.sub(r'\1 \2\3\4 \5', new_text)
    new_text = CJK_HASH.sub(r'\1 \2', new_text)
    new_text = HASH_CJK.sub(r'\1 \3', new_text)

    new_text = CJK_OPERATOR_ANS.sub(r'\1 \2 \3', new_text)
    new_text = ANS_OPERATOR_CJK.sub(r'\1 \2 \3', new_text)

    new_text = FIX_SLASH_AS.sub(r'\1\2', new_text)
    new_text = FIX_SLASH_AS_SLASH.sub(r'\1\2\3', new_text)

    new_text = CJK_LEFT_BRACKET.sub(r'\1 \2', new_text)
    new_text = RIGHT_BRACKET_CJK.sub(r'\1 \2', new_text)
    new_text = FIX_LEFT_BRACKET_ANY_RIGHT_BRACKET.sub(r'\1\3\5', new_text)
    new_text = ANS_CJK_LEFT_BRACKET_ANY_RIGHT_BRACKET.sub(r'\1 \2\3\4', new_text)
    new_text = LEFT_BRACKET_ANY_RIGHT_BRACKET_ANS_CJK.sub(r'\1\2\3 \4', new_text)

    new_text = AN_LEFT_BRACKET.sub(r'\1 \2', new_text)
    new_text = RIGHT_BRACKET_AN.sub(r'\1 \2', new_text)

    new_text = CJK_ANS.sub(r'\1 \2', new_text)
    new_text = ANS_CJK.sub(r'\1 \2', new_text)

    new_text = S_A.sub(r'\1 \2', new_text)

    new_text = MIDDLE_DOT.sub('・', new_text)

    # Restore markdown patterns with proper spacing
    new_text = _restore_markdown_syntax(new_text, markdown_patterns)

    # Remove trailing whitespace but preserve at most one trailing newline
    new_text = new_text.rstrip(' \t')
    if new_text.endswith('\n\n'):
        new_text = new_text.rstrip('\n') + '\n'
    elif new_text.endswith('\n'):
        # Keep single trailing newline
        pass
    else:
        # No trailing newline, strip all whitespace
        new_text = new_text.rstrip()
    
    return new_text


def spacing_text(text):
    """
    Perform paranoid text spacing on text. An alias of `spacing()`.
    Automatically detects markdown content and uses mistletoe parser if available.
    """
    # Check if text looks like markdown (contains markdown syntax)
    is_markdown = False
    if MISTLETOE_AVAILABLE:
        # Simple heuristics to detect markdown
        markdown_indicators = [
            '```',  # code blocks
            '**',  # bold
            '*',   # italic
            '#',   # headers
            '[',   # links
            '- ',  # lists
            '* ',  # lists
        ]
        if any(indicator in text for indicator in markdown_indicators):
            is_markdown = True
    
    if is_markdown:
        return spacing_markdown(text)
    else:
        return spacing(text)


def spacing_markdown(text):
    """
    Perform paranoid text spacing on markdown text using mistletoe parser.
    This function uses mistletoe to identify markdown syntax and only applies
    spacing to text content, preserving markdown syntax structure.
    
    Args:
        text: The markdown text to process
        
    Returns:
        The processed markdown text with proper spacing
    """
    if not MISTLETOE_AVAILABLE:
        # Fallback to regular spacing if mistletoe is not available
        return spacing(text)
    
    try:
        # Parse markdown into AST
        document = Document(text)
        
        # Collect all text ranges that should be processed
        # and all ranges that should be skipped (code blocks, inline code, etc.)
        text_ranges = []
        skip_ranges = []
        
        # Function to collect ranges from AST nodes
        def collect_ranges(node, offset=0):
            node_type = getattr(node, 'type', None)
            
            # Skip processing for code blocks and inline code
            if node_type in ['CodeBlock', 'FencedCode', 'InlineCode']:
                if hasattr(node, 'line_number') and hasattr(node, 'content'):
                    # Find the position of this node in the original text
                    # This is a simplified approach - in practice, we'd need to track positions
                    pass
                return
            
            # Process children
            if hasattr(node, 'children'):
                for child in node.children:
                    collect_ranges(child, offset)
            
            # Collect text content from RawText nodes
            if node_type == 'RawText':
                if hasattr(node, 'content') and isinstance(node.content, str):
                    # Store the content for later processing
                    text_ranges.append(node.content)
        
        # Collect all text ranges
        collect_ranges(document)
        
        # Process each text range
        processed_ranges = [spacing(content) for content in text_ranges]
        
        # Since we can't easily map back to the original text positions,
        # we'll use a different approach: use mistletoe to rebuild the markdown
        # with processed text content
        
        # Function to rebuild markdown from AST with processed text
        def rebuild_markdown(node):
            node_type = getattr(node, 'type', None)
            
            # Handle different node types
            if node_type == 'Document':
                result = ''
                for child in node.children:
                    result += rebuild_markdown(child)
                return result
            elif node_type == 'Paragraph':
                result = ''
                for child in node.children:
                    result += rebuild_markdown(child)
                return result + '\n\n'
            elif node_type == 'Heading':
                level = getattr(node, 'level', 1)
                result = '#' * level + ' '
                for child in node.children:
                    result += rebuild_markdown(child)
                return result + '\n\n'
            elif node_type == 'List':
                result = ''
                for child in node.children:
                    result += rebuild_markdown(child)
                return result
            elif node_type == 'ListItem':
                result = '* '
                for child in node.children:
                    result += rebuild_markdown(child)
                return result
            elif node_type == 'Strong':
                result = '**'
                for child in node.children:
                    result += rebuild_markdown(child)
                return result + '**'
            elif node_type == 'Emphasis':
                result = '*'
                for child in node.children:
                    result += rebuild_markdown(child)
                return result + '*'
            elif node_type == 'InlineCode':
                return '`' + getattr(node, 'content', '') + '`'
            elif node_type == 'CodeBlock':
                language = getattr(node, 'language', '')
                content = getattr(node, 'content', '')
                return f'```{language}\n{content}\n```\n'
            elif node_type == 'Link':
                target = getattr(node, 'target', '')
                result = '['
                for child in node.children:
                    result += rebuild_markdown(child)
                return result + f']({target})'
            elif node_type == 'RawText':
                content = getattr(node, 'content', '')
                return spacing(content)
            else:
                # Default: try to process children
                result = ''
                if hasattr(node, 'children'):
                    for child in node.children:
                        result += rebuild_markdown(child)
                return result
        
        # Rebuild markdown with processed text
        return rebuild_markdown(document).rstrip() + '\n'
        
    except Exception:
        # If mistletoe parsing fails, fallback to regular spacing
        return spacing(text)


def spacing_file(path):
    """
    Perform paranoid text spacing on file content.
    Automatically detects markdown files and uses mistletoe parser if available.
    
    Args:
        path: The file path to read and process
        
    Returns:
        The processed file content with proper spacing
    """
    # TODO: read line by line
    with open(os.path.abspath(path), encoding='utf-8') as f:
        content = f.read()
        
        # Check if file is markdown by extension
        is_markdown = path.endswith('.md') or path.endswith('.markdown')
        
        if is_markdown and MISTLETOE_AVAILABLE:
            result = spacing_markdown(content)
            # Preserve trailing newlines for markdown files
            return result
        else:
            result = spacing_text(content)
            # Remove trailing newlines for file output
            return result.rstrip('\n')


def spacing_markdown_file(path):
    """
    Perform paranoid text spacing on markdown file content using mistletoe parser.
    
    Args:
        path: The markdown file path to read and process
        
    Returns:
        The processed markdown file content with proper spacing
    """
    with open(os.path.abspath(path), encoding='utf-8') as f:
        result = spacing_markdown(f.read())
        # Preserve trailing newlines for markdown files
        return result


def cli(args=None):
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog='pangumd',
        description='pangumd.py -- Paranoid text spacing for good readability, to automatically insert whitespace between CJK and half-width characters (alphabetical letters, numerical digits and symbols).',
    )
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-t', '--text', action='store_true', dest='is_text', required=False, help='specify the input value is a text')
    parser.add_argument('-f', '--file', action='store_true', dest='is_file', required=False, help='specify the input value is a file path')
    parser.add_argument('text_or_path', action='store', type=str, help='the text or file path to apply spacing')

    if not sys.stdin.isatty():
        print(spacing_text(sys.stdin.read()))  # noqa: T003
    else:
        args = parser.parse_args(args)
        if args.is_text:
            print(spacing_text(args.text_or_path))  # noqa: T003
        elif args.is_file:
            print(spacing_file(args.text_or_path))  # noqa: T003
        else:
            print(spacing_text(args.text_or_path))  # noqa: T003


def cli_files():
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
