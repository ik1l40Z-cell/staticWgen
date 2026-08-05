import unittest
from htmlnode import HTMLNode, LeafNode

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

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, bald!")
        self.assertEqual(node.to_html(), "<b>Hello, bald!</b>")

    def test_leaf_to_html_no(self):
        node = LeafNode("b", "Hello, bald!", {"href": "https://www.youtube.com/dougdoug"})
        self.assertIsNone(node.children)

    def test_leaf_to_html_vlr(self):
        node = LeafNode("a", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, bald!")
        self.assertEqual(node.to_html(), "Hello, bald!")

    def test_leaf_to_html_itd(self):
        props = {
            "href": "https://www.youtube.com/dougdoug",
            "target": "_shaved"
        }
        node = LeafNode("a", "Hello, bald!", props)
        self.assertEqual(node.to_html(), '<a href="https://www.youtube.com/dougdoug" target="_shaved">Hello, bald!</a>')
