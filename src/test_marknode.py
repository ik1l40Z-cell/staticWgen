import unittest
from marknode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_xtr_md_imgs_solo(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_xtr_md_imgs_double(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        lit = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(lit, matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_xtr_md_liks_solo(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_xtr_md_liks_double(self):
        matches = extract_markdown_links(
            "Go to [the yellow book](https://www.yellowpages.com) to find anything and [the king in yellow](https://www.carcosa.gov) to lose it all !"
        )
        lit = [
            ("the yellow book", "https://www.yellowpages.com"),
            ("the king in yellow", "https://www.carcosa.gov"),
        ]
        self.assertListEqual(lit, matches)

    def test_xtr_md_liks_mixed(self):
        matches = extract_markdown_links(
            "Go to [the yellow book](https://www.yellowpages.com) to find anything and ![the king in yellow](https://www.carcosa.gov) to lose it all !"
        )
        lit = [
            ("the yellow book", "https://www.yellowpages.com"),
        ]
        self.assertListEqual(lit, matches)
