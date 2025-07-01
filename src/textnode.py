from enum import Enum

class TextType(Enum):
    PLAIN="plain"
    ITALIC="italic"
    BOLD="bold"
    CODE="code"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        
        if (text_type == TextType.LINK or text_type == TextType.IMAGE):
            self.url = url
        else:
            self.url = None
            
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        if(self.url is not None):
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        else: 
            return f"TextNode({self.text}, {self.text_type.value})"