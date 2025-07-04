from enum import Enum


# Define the StrEnum for HTML tags
class Tags(Enum):
    p = "p"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"
    h4 = "h4"
    h5 = "h5"
    h6 = "h6"
    pre = "pre"
    code = "code"
    blockquote = "blockquote"
    ul = "ul"
    ol = "ol"
    li = "li"
    b = "b"
    i = "i"
    a = "a"
    img = "img"
    div = "div"


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        return "".join([f' {k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
