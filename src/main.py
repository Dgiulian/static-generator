from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
import re


def main():
    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    node2 = TextNode("This is some anchor text", TextType.TEXT, "https://www.boot.dev")
    print(node)
    print(node == node2)


if __name__ == "__main__":
    main()
