from enum import Enum
import re


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split('\n')
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
