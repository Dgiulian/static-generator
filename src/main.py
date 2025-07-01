from textnode import TextNode,TextType

def main():
  node = TextNode("This is some anchor text", TextType.BOLD,"https://www.boot.dev")
  node2 = TextNode("This is some anchor text", TextType.PLAIN,"https://www.boot.dev")
  print(node)
  print(node == node2)


if __name__ == '__main__':
  main()
