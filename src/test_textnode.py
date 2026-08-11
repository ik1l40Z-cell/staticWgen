import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertEqual(node, node2)

    def test_aeq(self):
        node = TextNode(
            "This is a link node",
            TextType.LINK_TYPE,
            "https://www.google.com",
        )
        node2 = TextNode(
            "This is a link node",
            TextType.LINK_TYPE,
            "https://www.google.com",
        )
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode(
            "This is a not a node",
            TextType.IMAGE_TYPE,
            "https://www.google.com",
        )
        node2 = TextNode(
            "This is a image node",
            TextType.IMAGE_TYPE,
            "https://www.google.com",
        )
        self.assertNotEqual(node, node2)

    def test_beq(self):
        node = TextNode("This is a link node", TextType.LINK_TYPE, None)
        node2 = TextNode("This is a link node", TextType.LINK_TYPE, None)
        self.assertEqual(node, node2)

    def test_seq(self):
        node = TextNode(
            "This is a figure of speech",
            TextType.ITALIC_TYPE,
            "https://www.boot.dev",
        )
        node2 = TextNode(
            "This is a figure of speech",
            TextType.PLAIN_TYPE,
            "https://www.boot.dev",
        )
        self.assertNotEqual(node, node2)

    def test_text_b(self):
        node = TextNode("This is a thicc text node", TextType.BOLD_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a thicc text node")

    def test_text_i(self):
        node = TextNode("This is a lean text node", TextType.ITALIC_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a lean text node")

    def test_text_c(self):
        node = TextNode("This is a cryptic text node", TextType.CODE_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a cryptic text node")

    def test_text_l(self):
        node = TextNode(
            "This is an hyper-link node",
            TextType.LINK_TYPE,
            "https://www.ibm.com",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.ibm.com"})
        self.assertEqual(html_node.value, "This is an hyper-link node")

    def test_text_p(self):
        node = TextNode(
            "This is a digital picture node",
            TextType.IMAGE_TYPE,
            "https://www.x.com/7175&80085",
        )
        html_node = text_node_to_html_node(node)
        dictat = {
            "src": "https://www.x.com/7175&80085",
            "alt": "This is a digital picture node",
        }
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, dictat)


if __name__ == "__main__":
    unittest.main()
