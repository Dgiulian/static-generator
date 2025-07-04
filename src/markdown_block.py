import re
from enum import Enum
from splitting import markdown_to_blocks, text_to_textnodes
from htmlnode import HTMLNode, Tags
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    if len(lines) > 0:
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                is_ordered_list = False
                break
    else:
        is_ordered_list = False

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode(Tags.div, children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children: list[LeafNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = re.sub(" +", " ", " ".join(lines)).strip()
    children = text_to_children(paragraph)
    return ParentNode(Tags.p, children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    lines = text.split("\n")
    stripped_lines = [line.lstrip() for line in lines]
    content = "\n".join(stripped_lines)
    if content.startswith("\n"):
        content = content[1:]

    raw_text_node = TextNode(content, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode(Tags.code, [child])
    return ParentNode(Tags.pre, [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[ParentNode] = []
    for item in items:
        text = item[3:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode(Tags.li, children))
    return ParentNode(Tags.ol, html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[ParentNode] = []
    for item in items:
        text = item[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode(Tags.li, children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode(Tags.blockquote, children)


if __name__ == "__main__":
    md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

    node = markdown_to_html_node(md)
    print(node)
    html = node.to_html()
    print(
        html,
        # "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    # def test_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )


def extract_title(markdown):

    for l in markdown.split("\n"):
        if markdown.startswith("# "):
            return markdown[2:].strip()
    raise Exception("It's not a header")
