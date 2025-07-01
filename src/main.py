from textnode import TextNode,TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

def main():
  node = TextNode("This is some anchor text", TextType.BOLD,"https://www.boot.dev")
  node2 = TextNode("This is some anchor text", TextType.TEXT,"https://www.boot.dev")
  print(node)
  print(node == node2)


def text_node_to_html_node(text_node):
    if (text_node.text_type == TextType.TEXT):
    #This should return a LeafNode with no tag, just a raw text value.
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.BOLD: 
    #This should return a LeafNode with a "b" tag and the text
      return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC: 
      #"i" tag, text
      return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE: 
      #"code" tag, text
      return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK: 
      #"a" tag, anchor text, and "href" prop
      return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE: 
      #"img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text })

    raise Exception(f"Invalid text type: {text_node.text_type}")


if __name__ == '__main__':
  main()
