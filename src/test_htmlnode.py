import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_ceq(self):
        child = HTMLNode("p", "Do you know the way ?")
        parent = HTMLNode("a", None, [child], {"href": "https://www.google.com"})
        self.assertEqual(parent.children, [child])

    def test_rs(self):
        node = HTMLNode("p", "Do you know the way ?")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_no(self):
        node = HTMLNode("a", "Do you know the way ?", None)
        self.assertIsNone(node.children)

    def test_nl(self):
        node = HTMLNode("a", "Do you know the way ?", [HTMLNode("p", "No way, Jose.")])
        empty = node.props_to_html()
        self.assertEqual(empty, "")

    def test_in(self):
        node = HTMLNode("a", "Do you know the way ?", None, {"target": "_blank", "href": "https://www.google.com"})
        format = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', format)
