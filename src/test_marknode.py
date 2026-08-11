import unittest
from marknode import split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_base(self):
        olnod = [
            TextNode(
                "Let bygones be by **Goons** !",
                TextType.PLAIN_TYPE,
            ),
        ]
        nunod = split_nodes_delimiter(
            olnod,
            "**",
            TextType.BOLD_TYPE,
        )
        rezz = [
            TextNode(
                "Let bygones be by ",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Goons",
                TextType.BOLD_TYPE,
            ),
            TextNode(
                " !",
                TextType.PLAIN_TYPE,
            ),
        ]
        self.assertEqual(nunod, rezz)

    def test_big(self):
        olnod = [
            TextNode(
                "Let bygones be by _Goons_ !",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
		"Be _Goon_ you vile _Beast !_",
		TextType.PLAIN_TYPE,
            ),
        ]
        nunod = split_nodes_delimiter(
            olnod,
            "_",
            TextType.ITALIC_TYPE,
        )
        rezz = [
            TextNode(
                "Let bygones be by ",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Goons",
                TextType.ITALIC_TYPE,
            ),
            TextNode(
                " !",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Be ",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Goon",
                TextType.ITALIC_TYPE,
            ),
            TextNode(
                " you vile ",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Beast !",
                TextType.ITALIC_TYPE,
            ),
        ]
        self.assertEqual(nunod, rezz)

    def test_tiny(self):
        olnod = [TextNode("`exit`", TextType.PLAIN_TYPE)]
        nunod = split_nodes_delimiter(olnod, "`", TextType.CODE_TYPE)
        rezz = [TextNode("exit", TextType.CODE_TYPE)]
        self.assertEqual(nunod, rezz)

    def test_plain(self):
        olnod = [TextNode("mixit", TextType.PLAIN_TYPE)]
        nunod = split_nodes_delimiter(olnod, "_", TextType.PLAIN_TYPE)
        rezz = [TextNode("mixit", TextType.PLAIN_TYPE)]
        self.assertEqual(nunod, rezz)

    def test_err(self):
        olnod = [TextNode("**dig**it**", TextType.PLAIN_TYPE)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(olnod, "**", TextType.BOLD_TYPE)
