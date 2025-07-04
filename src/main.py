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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.isdir(dir_path_content):
        print(f"{dir_path_content} is not adirectory")
        raise Exception(f"{dir_path_content} is not adirectory")

    for l in os.listdir(dir_path_content):
        new_from = os.path.join(dir_path_content, l)
        new_dest = os.path.join(dest_dir_path, l)
        if os.path.isfile(new_from) and new_from.endswith(".md"):

            dest_file = os.path.join(dest_dir_path, l.replace(".md", ".html"))

            generate_page(
                from_path=new_from,
                template_path=template_path,
                dest_path=dest_file,
            )
        elif os.path.isdir(new_from):
            if not os.path.exists(new_dest):
                os.makedirs(new_dest)
            generate_pages_recursive(
                dir_path_content=new_from,
                template_path=template_path,
                dest_dir_path=new_dest,
            )
        else:
            print(f"Nothing to do with {new_from} and {new_dest}")
            print(f"Nothing to do with {new_from} and {new_dest}")


def main():
    source = "static"
    dest = "public"

    deleteContent(dest)
    copyContent(source, dest)
    generate_pages_recursive(
        dir_path_content=os.path.join("content"),
        template_path=os.path.join("template.html"),
        dest_dir_path=os.path.join("public"),
    )


if __name__ == "__main__":
    main()
