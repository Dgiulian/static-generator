import unittest

from markdown_block import BlockType, block_to_block_type


class TestMarkdownBlock(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "#### Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "##### Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nCode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_mixed(self):
        block = "- Item 1\n1. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
