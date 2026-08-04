import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertEqual(node, node2)

    def test_aeq(self):
        node = TextNode("This is a link node", TextType.LINK_TYPE, "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK_TYPE, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a not a node", TextType.IMAGE_TYPE, "https://www.google.com")
        node2 = TextNode("This is a image node", TextType.IMAGE_TYPE, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_beq(self):
        node = TextNode("This is a link node", TextType.LINK_TYPE, None)
        node2 = TextNode("This is a link node", TextType.LINK_TYPE, None)
        self.assertEqual(node, node2)

    def test_seq(self):
        node = TextNode("This is a figure of speech", TextType.ITALIC_TYPE, "https://www.boot.dev")
        node2 = TextNode("This is a figure of speech", TextType.PLAIN_TYPE, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
