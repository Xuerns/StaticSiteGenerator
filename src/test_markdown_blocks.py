import unittest
from markdown_blocks import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is block 1




This is block 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block 1",
                "This is block 2",
            ],
        )

    def test_markdown_to_blocks_single(self):
        md = "Just a single paragraph without any blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just a single paragraph without any blank lines."],
        )

    def test_markdown_to_blocks_empty(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block2 = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block2), BlockType.CODE)
        block3 = "```inline```"
        self.assertEqual(block_to_block_type(block3), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = ">quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block_invalid = ">quote line 1\nnot quote"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block_invalid = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block_invalid = "1. first\n3. second"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)
        block_invalid2 = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block_invalid2), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

### Heading 3 with **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3 with <b>bold</b></h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote block
> with multiple lines and **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block with multiple lines and <b>bold</b></blockquote></div>",
        )

    def test_lists(self):
        md = """
- Item 1
- Item 2 with _italic_

1. First item
2. Second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <i>italic</i></li></ul><ol><li>First item</li><li>Second item</li></ol></div>",
        )


    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_with_spaces(self):
        self.assertEqual(extract_title("#   Tolkien Fan Club   "), "Tolkien Fan Club")

    def test_extract_title_multiline(self):
        md = "Introductory text\n\n# Main Title\n\nSome more paragraphs"
        self.assertEqual(extract_title(md), "Main Title")

    def test_extract_title_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Only h2\n### And h3")


if __name__ == "__main__":
    unittest.main()


