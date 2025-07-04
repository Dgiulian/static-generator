from htmlnode import HTMLNode
from enum import Enum

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)


  def to_html(self):
    if(self.tag is None):
      raise ValueError()
    
    if(self.children is None):
      raise ValueError()
    
    children_html = ""
    for child in self.children:
      children_html += child.to_html()

    tag = self.tag
    if isinstance(self.tag, Enum):
      tag = self.tag.value

    return f"<{tag}{self.props_to_html()}>{children_html}</{tag}>"