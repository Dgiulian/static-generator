import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "This is a paragraph of text.",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode(
            "p",
            "This is a paragraph of text.",
            None,
            None,
        )
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph of text.", None, {"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(p, This is a paragraph of text., None, {'class': 'my-class'})")

if __name__ == "__main__":
    unittest.main()