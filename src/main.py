from textnode import TextNode, TextType
import re
import os
import shutil
from markdown_block import markdown_to_html_node, extract_title


def copyContent(sourceDir, destDir):
    if not os.path.exists(destDir):
        os.mkdir(destDir)

    for i in os.listdir(sourceDir):
        sourcePath = os.path.join(sourceDir, i)
        destPath = os.path.join(destDir, i)
        if os.path.isfile(sourcePath):
            shutil.copy(sourcePath, destPath)
        else:
            copyContent(sourcePath, destPath)


def deleteContent(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as fp:
        markdown = fp.read()

    with open(template_path, "r") as t:
        template = t.read()

    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()

    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as d:
        d.write(template)


def main():
    source = "static"
    dest = "public"

    deleteContent(dest)
    copyContent(source, dest)
    generate_page(
        from_path=os.path.join("content", "index.md"),
        template_path=os.path.join("template.html"),
        dest_path=os.path.join("public", "index.html"),
    )


if __name__ == "__main__":
    main()

    copyContent("static", "public")


if __name__ == "__main__":
    main()
