import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_no_value(self):
        leaf = LeafNode(None, "a") 
        leaf.value = None
        with self.assertRaises(ValueError) as ctx:
            leaf.to_html()
    

    def test_to_html1(self):
        expected = "<p>This is a paragraph of text.</p>"
        leaf = LeafNode("p", "This is a paragraph of text.")
        result = leaf.to_html()
        self.assertEqual(expected, result)


    def test_to_html2(self):
        expected = '<a href="https://www.google.com">Click me!</a>'
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = leaf.to_html()
        self.assertEqual(expected, result)


    def test_to_html3(self):
        expected = "This is a test"
        leaf = LeafNode(None, "This is a test")
        result = leaf.to_html()
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()