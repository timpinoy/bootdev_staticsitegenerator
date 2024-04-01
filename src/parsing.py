import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

from textnode import (
    text_node_to_html_node
)


markdown_type_paragraph = "paragraph"
markdown_type_heading = "heading"
markdown_type_code = "code"
markdown_type_quote = "quote"
markdown_type_unordered_list = "unordered_list"
markdown_type_ordered_list = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            ret_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception("Invalid markdown syntax")
            for i in range(0, len(split_nodes)):
                if split_nodes[i] != "":
                    if i % 2 == 0:
                        ret_nodes.append(TextNode(split_nodes[i], text_type_text)) 
                    else:
                        ret_nodes.append(TextNode(split_nodes[i], text_type))
    return ret_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    return_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            return_nodes.append(old_node)
            continue
        curr_text = old_node.text
        for image in images:
            if curr_text == "":
                continue
            split_text = curr_text.split(f"![{image[0]}]({image[1]})", 1)
            if split_text[0] != "":
                return_nodes.append(TextNode(split_text[0], text_type_text))
            return_nodes.append(TextNode(image[0], text_type_image, image[1]))
            curr_text = split_text[1]
        if curr_text != "":
            return_nodes.append(TextNode(curr_text, text_type_text))
    return return_nodes

def split_nodes_link(old_nodes):
    return_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            return_nodes.append(old_node)
            continue
        curr_text = old_node.text
        for link in links:
            if curr_text == "":
                continue
            split_text = curr_text.split(f"[{link[0]}]({link[1]})", 1)
            if split_text[0] != "":
                return_nodes.append(TextNode(split_text[0], text_type_text))
            return_nodes.append(TextNode(link[0], text_type_link, link[1]))
            curr_text = split_text[1]
        if curr_text != "":
            return_nodes.append(TextNode(curr_text, text_type_text))
    return return_nodes

def text_to_textnodes(text):
    return_nodes = [TextNode(text, text_type_text)]
    return_nodes = split_nodes_delimiter(return_nodes, "**", text_type_bold)
    return_nodes = split_nodes_delimiter(return_nodes, '*', text_type_italic)
    return_nodes = split_nodes_delimiter(return_nodes, "`", text_type_code)
    return_nodes = split_nodes_image(return_nodes)
    return_nodes = split_nodes_link(return_nodes)
    return return_nodes

def markdown_to_blocks(markdown):
    result = []
    for block in markdown.split("\n\n"):
        cleaned = block.strip()
        if cleaned != "":
            result.append(cleaned)
    return result

def block_to_block_type(block):
    if re.search(r"^\#{1,6} ", block) != None:
        return markdown_type_heading
    if re.search(r"^`{3}.*`{3}$", block, flags=re.DOTALL):
        return markdown_type_code
    lines = block.split("\n")
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    for i in range(0, len(lines)):
        if lines[i][0] != ">":
            is_quote = False
        if not (lines[i][0] == "*" or lines[i][0] == "-"):
            is_unordered_list = False
        if not (lines[i][1] == "." and lines[i][0] == f"{i+1}"):
            is_ordered_list = False
    if is_quote:
        return markdown_type_quote
    if is_unordered_list:
        return markdown_type_unordered_list
    if is_ordered_list:
        return markdown_type_ordered_list

    return markdown_type_paragraph

def markdown_quote_to_html_node(block):
    return LeafNode("blockquote", block.replace(">", "").strip())

def markdown_ul_to_html_node(block):
    parent = ParentNode("ul", [])
    for li in block.split("\n"):
        item = ParentNode("li", [])
        for text_node in text_to_textnodes(li[1:].strip()):
            item.children.append(text_node_to_html_node(text_node))
        parent.children.append(item)
    return parent

def markdown_ol_to_html_node(block):
    parent = ParentNode("ol", [])
    for li in block.split("\n"):
        item = ParentNode("li", [])
        for text_node in text_to_textnodes(li[2:].strip()):
            item.children.append(text_node_to_html_node(text_node))
        parent.children.append(item)
    return parent

def markdown_code_to_html_node(block):
    text = block.replace("```", "").strip()
    pre_parent = ParentNode("pre", [])
    code_parent = ParentNode("code", [])
    for text_node in text_to_textnodes(text):
        code_parent.children.append(text_node_to_html_node(text_node))
    pre_parent.children.append(code_parent)
    return pre_parent

def markdown_heading_to_html_node(block):
    split_block = block.split(" ")
    heading = ParentNode(f"h{len(split_block[0])}", [])
    for text_node in text_to_textnodes(" ".join(split_block[1:])):
        heading.children.append(text_node_to_html_node(text_node))
    return heading

def markdown_paragraph_to_html_node(block):
    html_nodes = ParentNode("p", [])
    text_nodes = text_to_textnodes(block)
    for text_node in text_nodes:
        html_nodes.children.append(text_node_to_html_node(text_node))
    return html_nodes    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    main_parent = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == markdown_type_quote:
            main_parent.children.append(markdown_quote_to_html_node(block))

        if block_type == markdown_type_unordered_list:
            main_parent.children.append(markdown_ul_to_html_node(block))

        if block_type == markdown_type_ordered_list:
            main_parent.children.append(markdown_ol_to_html_node(block))

        if block_type == markdown_type_code:
            main_parent.children.append(markdown_code_to_html_node(block))

        if block_type == markdown_type_heading:
            main_parent.children.append(markdown_heading_to_html_node(block))

        if block_type == markdown_type_paragraph:
            main_parent.children.append(markdown_paragraph_to_html_node(block))

    return main_parent

def extract_title(markdown):
    for line in markdown.split("\n"):
        if re.search(r"^#{1}", line) != None:
            return line[1:].strip()
    raise Exception("Expecting at least one h1 header")