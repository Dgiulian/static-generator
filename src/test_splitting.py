import unittest

from textnode import TextNode, TextType
from splitting import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)


class TestSplitting(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode("This is **bold** and **again**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("again", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode("_italic_ and _more_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("more", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No special formatting here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_multiple_nodes(self):
        node1 = TextNode("A `code` test", TextType.TEXT)
        node2 = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" test", TextType.TEXT),
            TextNode("**bold**", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("irrelevant", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_unclosed_delimiter(self):
        node = TextNode("`unclosed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_no_links(self):
        node = TextNode("This is text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![image](https.png) some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https.png"),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("some text [link](https.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text with no markdown."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is plain text with no markdown.", TextType.TEXT)], nodes
        )

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_only_image(self):
        text = "An ![image](https://example.com/image.png) here."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("An ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" here.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_same_type(self):
        text = "**Bold1** and **Bold2** and *Italic1* and *Italic2*."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("Bold2", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("Italic1", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("Italic2", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_markdown_at_start_end(self):
        text = "**Start** and end with a [link](https://end.com)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Start", TextType.BOLD),
                TextNode(" and end with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://end.com"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

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

    def test_markdown_to_blocks_spaces(self):
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
