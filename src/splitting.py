import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = re.split(f"({re.escape(delimiter)})", old_node.text)

        if parts.count(delimiter) % 2 != 0:
            raise ValueError("Invalid markdown, unclosed delimiter")

        i = 0
        while i < len(parts):
            part = parts[i]
            if part == "":
                i += 1
                continue

            if part == delimiter:
                new_nodes.append(TextNode(parts[i + 1], text_type))
                i += 2  # Skip the content part as well
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
            i += 1
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if not images:
            new_nodes.append(old_node)
            continue

        text_to_process = original_text
        for alt_text, url in images:
            markdown_image = f"![{alt_text}]({url})"
            parts = text_to_process.split(markdown_image, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            text_to_process = parts[1]

        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if not links:
            new_nodes.append(old_node)
            continue

        text_to_process = original_text
        for alt_text, url in links:
            markdown_link = f"[{alt_text}]({url})"
            parts = text_to_process.split(markdown_link, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            text_to_process = parts[1]

        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown):
    blocks = [b.strip() for b in markdown.split("\n\n") if b.strip() != ""]
    return blocks


if __name__ == "__main__":
    print(
        markdown_to_blocks(
            """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item






However this should be removed


But not this
"""
        )
    )
