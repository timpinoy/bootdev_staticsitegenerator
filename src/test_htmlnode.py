import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
   def test_repr(self):
       n = HTMLNode("tag", "value", "children", "props")
       str = n.__repr__()
       self.assertEqual(str, "HTMLNode(tag, value, children, props)")


if __name__ == "__main__":
    unittest.main()