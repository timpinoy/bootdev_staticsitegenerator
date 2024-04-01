from parsing import (
    markdown_type_heading,
    markdown_type_code,
    markdown_type_ordered_list,
    markdown_type_unordered_list,
    markdown_type_paragraph,
    markdown_type_quote,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

import unittest

class TestParsing(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_exception(self):
        node = TextNode("This is text with a `invalid syntax", "text")
        with self.assertRaises(Exception) as ctx:
            new_nodes = split_nodes_delimiter([node], "`", "code")

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)


    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        result = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(result, expected_result)


    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
        ]
        self.assertEqual(result, expected_result)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)" 
        expected_result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)
    
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph   



This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items



"""
        result = markdown_to_blocks(markdown)
        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        self.assertEqual(result, expected_result)

    def test_block_to_block_type_heading1(self):
        block = "### a header"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_heading)

    def test_block_to_block_type_heading2(self):
        block = "###Not a header"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_paragraph)

    def test_block_to_block_type_code1(self):
        block = "```This is a code block```"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_code)

    def test_block_to_block_type_code2(self):
        block = """```This is a 
        multiline code block```"""
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_code)

    def test_block_to_block_type_code3(self):
        block = "```This is not a code block`"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_paragraph)

    def test_block_to_block_type_quote1(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_quote)

    def test_block_to_block_type_quote2(self):
        block = "> This is not a quote\nsecond line"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_paragraph)

    def test_block_to_block_type_quote3(self):
        block = "> This is a\n> multi-line quote"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_quote)

    def test_block_to_block_type_unordered_list1(self):
        block = "*this is\n*a unordered\n-list"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_unordered_list)

    def test_block_to_block_type_unordered_list2(self):
        block = "*this is\n*not a unordered\n#list"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_paragraph)

    def test_block_to_block_type_ordered_list1(self):
        block = "1.this is\n2.a ordered\3.list"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_ordered_list)

    def test_block_to_block_type_ordered_list2(self):
        block = "1.this is\n2.not a unordered\n4.list"
        result = block_to_block_type(block)
        self.assertEqual(result, markdown_type_paragraph)


if __name__ == "__main__":
    unittest.main()