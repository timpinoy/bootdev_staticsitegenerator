import os
import shutil
from parsing import (
    extract_title,
    markdown_to_html_node,
)

from htmlnode import HTMLNode


def main():
    public_dir_path = get_path("public")
    static_dir_path = get_path("static")
    content_dir_path = get_path("content")
    
    # clean up existing public folder
    if os.path.exists(public_dir_path):
        print("--- Removing existing public folder ---")
        shutil.rmtree(public_dir_path)
        print("\tDone")
    
    # copy from static to public
    print("--- Copying files from static to public ---")
    copy_dir_contents(static_dir_path, public_dir_path)
    print("\tDone")
    
    # generate HTML
    print("--- Generating HTML from markdown ---")
    template_path = os.path.join(get_path(""), "template.html")
    generate_pages_recursive(content_dir_path, template_path, public_dir_path)

def get_path(folder):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    return os.path.join(parent_dir, folder)

def copy_dir_contents(from_dir, to_dir):
    os.mkdir(to_dir)
    if not os.path.exists(from_dir):
        raise Exception("from directory does not exist")
    for i in os.listdir(from_dir):
        from_path = os.path.join(from_dir, i)
        to_path = os.path.join(to_dir, i)
        if os.path.isfile(from_path):
            print(f"\tCopying {from_path} to {to_path}")
            shutil.copy(from_path, to_path)
        if os.path.isdir(from_path):
            copy_dir_contents(from_path, to_path)

def generate_page(from_path, template_path, dest_path):
    print(f"\tGenerating page from {from_path} to {dest_path} using {template_path}...")
    from_file = open(from_path)
    md_text = from_file.read()
    template_file = open(template_path)
    template_text = template_file.read()
    generated_html = markdown_to_html_node(md_text).to_html()
    title = extract_title(md_text)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_file = open(dest_path, mode='w')
    dest_file.write(template_text.replace("{{ Title }}", title).replace("{{ Content }}", generated_html))
    dest_file.close()
    template_file.close()
    from_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Content path does not exist")
    for i in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, i)
        to_path = os.path.join(dest_dir_path, i)
        if os.path.isfile(from_path):
            path_root, _ = os.path.splitext(to_path)
            generate_page(from_path, template_path, path_root + ".html")
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path,template_path, to_path)


main()