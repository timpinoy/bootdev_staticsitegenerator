import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    
    def test_eq2(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node", "bold", "url")
        self.assertEqual(node, node2)
    
    
    def test_not_eq1(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node2", "bold")
        self.assertNotEqual(node, node2)


    def test_not_eq2(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)


    def test_not_eq3(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node2", "bold", None)
        self.assertNotEqual(node, node2)


    def test_repr(self):
        node = TextNode("This is a text node", "bold", "url")
        text = "TextNode(This is a text node, bold, url)"
        self.assertEqual(node.__repr__(), text)


if __name__ == "__main__":
    unittest.main()
