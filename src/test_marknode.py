import unittest
from marknode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from marknode import split_nodes_images, split_nodes_links, text_to_textnodes
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

class TestSplitNodesImages(unittest.TestCase):
    def test_splimages_simple(self):
        olnod = TextNode(
            "The mood I got, ![up-ladder](https://i.imgur.com/shVKO7E.jpeg)"
            " not the one I greened !",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode("The mood I got, ", TextType.PLAIN_TYPE),
            TextNode(
                "up-ladder",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/shVKO7E.jpeg",
            ),
            TextNode(" not the one I greened !", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_layers(self):
        olnod = TextNode(
            "Let them cook, he said...![actions have](https://i.imgur.com"
            "/kq2Qxz0.jpeg) Now we're hunted down !![dire consequences]"
            "(https://i.imgur.com/IPfGqet.jpeg) Ah! He got the Suskiki bros.",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode("Let them cook, he said...", TextType.PLAIN_TYPE),
            TextNode(
                "actions have",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/kq2Qxz0.jpeg",
            ),
            TextNode(" Now we're hunted down !", TextType.PLAIN_TYPE),
            TextNode(
                "dire consequences",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/IPfGqet.jpeg",
            ),
            TextNode(" Ah! He got the Suskiki bros.", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_flushed(self):
        olnod = TextNode("This is a picture of a horse: [honse]", TextType.PLAIN_TYPE)
        nunod = split_nodes_images([olnod])
        self.assertListEqual(nunod, [olnod])

    def test_splimages_early(self):
        olnod = TextNode(
            "![Early-Bird](https://i.imgur.com/baDT1A9.png) "
            "takes the wasp's ahh !",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode(
                "Early-Bird",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/baDT1A9.png"
            ),
            TextNode(" takes the wasp's ahh !", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_later(self):
        olnod = TextNode(
            "Smooth as leather, hey.. Later! Aligator."
            "![Later-Gator](https://i.imgur.com/8tWdWj2.jpeg)",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode("Smooth as leather, hey.. Later! Aligator.", TextType.PLAIN_TYPE),
            TextNode(
                "Later-Gator",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/8tWdWj2.jpeg",
            ),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_bum2bum(self):
        olnod = TextNode(
            "Here are two unrelated ![racoon citizen](https://i.imgur.com/qJakA8P.jpeg)![t"
            "he plite of tell](https://i.imgur.com/pdy1qem.jpeg) pics about stuff...",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode("Here are two unrelated ", TextType.PLAIN_TYPE),
            TextNode(
                "racoon citizen",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/qJakA8P.jpeg",
            ),
            TextNode(
                "the plite of tell",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/pdy1qem.jpeg",
            ),
            TextNode(" pics about stuff...", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_unplain(self):
        olnod = TextNode(
            "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
            TextType.CODE_TYPE,
        )
        nunod = split_nodes_images([olnod])
        self.assertListEqual(nunod, [olnod])

    def test_splimages_null(self):
        nunod = split_nodes_images([])
        self.assertListEqual(nunod, [])

    def test_splimages_multed(self):
        self.maxDiff = None
        olnod = [
            TextNode(
                "The mood I got, ![up-ladder](https://i.imgur.com/shVKO7E.jpeg)"
                " not the one I greened !",
                TextType.PLAIN_TYPE,
            ),
            TextNode(" 1337 ", TextType.ITALIC_TYPE),
            TextNode(
                "Smooth as leather, hey.. Later! Aligator."
                "![Later-Gator](https://i.imgur.com/8tWdWj2.jpeg)",
                TextType.PLAIN_TYPE,
            ),
            TextNode(" 800845 1! ", TextType.BOLD_TYPE),
            TextNode("This is a picture of a horse: [honse]", TextType.PLAIN_TYPE),
            TextNode(
                "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
                TextType.CODE_TYPE,
            ),
            TextNode(
                "Here are two unrelated ![racoon citizen](https://i.imgur.com/qJakA8P.jpeg)!"
                "[the plite of tell](https://i.imgur.com/pdy1qem.jpeg) pics about stuff...",
                TextType.PLAIN_TYPE,
            ),
        ]
        nunod = split_nodes_images(olnod)
        renod = [
            TextNode("The mood I got, ", TextType.PLAIN_TYPE),
            TextNode(
                "up-ladder",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/shVKO7E.jpeg",
            ),
            TextNode(" not the one I greened !", TextType.PLAIN_TYPE),
            TextNode(" 1337 ", TextType.ITALIC_TYPE),
            TextNode("Smooth as leather, hey.. Later! Aligator.", TextType.PLAIN_TYPE),
            TextNode(
                "Later-Gator",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/8tWdWj2.jpeg",
            ),
            TextNode(" 800845 1! ", TextType.BOLD_TYPE),
            TextNode("This is a picture of a horse: [honse]", TextType.PLAIN_TYPE),
            TextNode(
                "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
                TextType.CODE_TYPE,
            ),
            TextNode("Here are two unrelated ", TextType.PLAIN_TYPE),
            TextNode(
                "racoon citizen",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/qJakA8P.jpeg",
            ),
            TextNode(
                "the plite of tell",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/pdy1qem.jpeg",
            ),
            TextNode(" pics about stuff...", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splimages_mixxed(self):
        olnod = TextNode(
            "Let them cook, he said...[actions have](https://www.x.com"
            "/Tide-pod) Now we're hunted down !![dire consequences]"
            "(https://i.imgur.com/IPfGqet.jpeg) Ah! He got the Suskiki bros.",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_images([olnod])
        renod = [
            TextNode(
                "Let them cook, he said...[actions have](https://www.x.com/Tide-pod)"
                " Now we're hunted down !",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "dire consequences",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/IPfGqet.jpeg",
            ),
            TextNode(" Ah! He got the Suskiki bros.", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

class TestSplitNodesLinks(unittest.TestCase):
    def test_splinks_simple(self):
        olnod = TextNode(
            "The mood I got, [up-ladder](https://merch.broke-boys.com)"
            " not the one I greened !",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode("The mood I got, ", TextType.PLAIN_TYPE),
            TextNode(
                "up-ladder",
                TextType.LINK_TYPE,
                "https://merch.broke-boys.com",
            ),
            TextNode(" not the one I greened !", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_layers(self):
        olnod = TextNode(
            "Let them cook, he said...[actions have](https://gemini.google.com"
            "/app) Now we're hunted down ! [dire consequences](https:/"
            "/www.rokosbasic-bitch.net) Ah! She got the Suskiki bros.",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode("Let them cook, he said...", TextType.PLAIN_TYPE),
            TextNode(
                "actions have",
                TextType.LINK_TYPE,
                "https://gemini.google.com/app",
            ),
            TextNode(" Now we're hunted down ! ", TextType.PLAIN_TYPE),
            TextNode(
                "dire consequences",
                TextType.LINK_TYPE,
                "https://www.rokosbasic-bitch.net",
            ),
            TextNode(" Ah! She got the Suskiki bros.", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_flushed(self):
        olnod = TextNode("This is a site about a horse: [juan.es]", TextType.PLAIN_TYPE)
        nunod = split_nodes_links([olnod])
        renod = [TextNode("This is a site about a horse: [juan.es]", TextType.PLAIN_TYPE)]
        self.assertListEqual(nunod, renod)

    def test_splinks_early(self):
        olnod = TextNode(
            "[Early-Bird](https://www.myspace.com) "
            "takes the wasp's ahh !",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode(
                "Early-Bird",
                TextType.LINK_TYPE,
                "https://www.myspace.com"
            ),
            TextNode(" takes the wasp's ahh !", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_later(self):
        olnod = TextNode(
            "Smooth as leather, hey.. Later! Aligator"
            ".[Later-Gator](https://www.tumblr.com)",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode("Smooth as leather, hey.. Later! Aligator.", TextType.PLAIN_TYPE),
            TextNode(
                "Later-Gator",
                TextType.LINK_TYPE,
                "https://www.tumblr.com",
            ),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_bum2bum(self):
        olnod = TextNode(
            "Here are two unrelated [rat city](https://www.wikihow.com)[t"
            "he plite of tell](https://www.wikipedia.org) sites about stuff...",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode("Here are two unrelated ", TextType.PLAIN_TYPE),
            TextNode(
                "rat city",
                TextType.LINK_TYPE,
                "https://www.wikihow.com",
            ),
            TextNode(
                "the plite of tell",
                TextType.LINK_TYPE,
                "https://www.wikipedia.org",
            ),
            TextNode(" sites about stuff...", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_unplain(self):
        olnod = TextNode(
            "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
            TextType.CODE_TYPE,
        )
        nunod = split_nodes_links([olnod])
        self.assertListEqual(nunod, [olnod])

    def test_splinks_null(self):
        nunod = split_nodes_links([])
        self.assertListEqual(nunod, [])

    def test_splinks_multed(self):
        self.maxDiff = None
        olnod = [
            TextNode(
                "Let them cook, he said...[actions have](https://gemini.google.com"
                "/app) Now we're hunted down ! [dire consequences](https:/"
                "/www.rokosbasic-bitch.net) Ah! She got the Suskiki bros.",
                TextType.PLAIN_TYPE,
            ),
            TextNode(" 1337 ", TextType.ITALIC_TYPE),
            TextNode(
                "[Early-Bird](https://www.myspace.com) "
                "takes the wasp's ahh !",
                TextType.PLAIN_TYPE,
            ),
            TextNode(" 800845 1!", TextType.BOLD_TYPE),
            TextNode("This is a site about a horse: [juan.es]", TextType.PLAIN_TYPE),
            TextNode(
                "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
                TextType.CODE_TYPE,
            ),
            TextNode(
                "Here are two unrelated [rat city](https://www.wikihow.com)[t"
                "he plite of tell](https://www.wikipedia.org) sites about stuff...",
                TextType.PLAIN_TYPE,
            ),
        ]
        nunod = split_nodes_links(olnod)
        renod = [
            TextNode("Let them cook, he said...", TextType.PLAIN_TYPE),
            TextNode(
                "actions have",
                TextType.LINK_TYPE,
                "https://gemini.google.com/app",
            ),
            TextNode(" Now we're hunted down ! ", TextType.PLAIN_TYPE),
            TextNode(
                "dire consequences",
                TextType.LINK_TYPE,
                "https://www.rokosbasic-bitch.net",
            ),
            TextNode(" Ah! She got the Suskiki bros.", TextType.PLAIN_TYPE),
            TextNode(" 1337 ", TextType.ITALIC_TYPE),
            TextNode(
                "Early-Bird",
                TextType.LINK_TYPE,
                "https://www.myspace.com"
            ),
            TextNode(" takes the wasp's ahh !", TextType.PLAIN_TYPE),
            TextNode(" 800845 1!", TextType.BOLD_TYPE),
            TextNode("This is a site about a horse: [juan.es]", TextType.PLAIN_TYPE),
            TextNode(
                "\nfor t in tests:\n    if t > 9000:\n        scooter[t].pop()\n",
                TextType.CODE_TYPE,
            ),
            TextNode("Here are two unrelated ", TextType.PLAIN_TYPE),
            TextNode(
                "rat city",
                TextType.LINK_TYPE,
                "https://www.wikihow.com",
            ),
            TextNode(
                "the plite of tell",
                TextType.LINK_TYPE,
                "https://www.wikipedia.org",
            ),
            TextNode(" sites about stuff...", TextType.PLAIN_TYPE),
        ]
        self.assertListEqual(nunod, renod)

    def test_splinks_mixxed(self):
        olnod = TextNode(
            "![Early-Bird](https://i.imgur.com/baDT1A9.png) "
            "takes the wasp's ahh ! Smooth as leather, hey.. Later! Aligator"
            ".[Later-Gator](https://www.tumblr.com)",
            TextType.PLAIN_TYPE,
        )
        nunod = split_nodes_links([olnod])
        renod = [
            TextNode(
                "![Early-Bird](https://i.imgur.com/baDT1A9.png) takes "
                "the wasp's ahh ! Smooth as leather, hey.. Later! Aligator.",
                TextType.PLAIN_TYPE,
            ),
            TextNode(
                "Later-Gator",
                TextType.LINK_TYPE,
                "https://www.tumblr.com",
            ),
        ]
        self.assertListEqual(nunod, renod)

class TestTextToTextnodes(unittest.TestCase):
    def test_ttt_plain(self):
        node = TextNode(
            "There is nothing special here.",
            TextType.PLAIN_TYPE,
        )
        self.assertEqual(text_to_textnodes("There is nothing special here."), [node])

    def test_ttt_triple(self):
        text = "There is _something_ special here, `while True:` it is of no **matter !**"
        node = [
            TextNode("There is ", TextType.PLAIN_TYPE),
            TextNode("something", TextType.ITALIC_TYPE),
            TextNode(" special here, ", TextType.PLAIN_TYPE),
            TextNode("while True:", TextType.CODE_TYPE),
            TextNode(" it is of no ", TextType.PLAIN_TYPE),
            TextNode("matter !", TextType.BOLD_TYPE),
        ]
        self.assertEqual(text_to_textnodes(text), node)

    def test_ttt_mixxed(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an ![obi "
            "wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        node = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode("text", TextType.BOLD_TYPE),
            TextNode(" with an ", TextType.PLAIN_TYPE),
            TextNode("italic", TextType.ITALIC_TYPE),
            TextNode(" word and a ", TextType.PLAIN_TYPE),
            TextNode("code block", TextType.CODE_TYPE),
            TextNode(" and an ", TextType.PLAIN_TYPE),
            TextNode(
                "obi wan image",
                TextType.IMAGE_TYPE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.PLAIN_TYPE),
            TextNode("link", TextType.LINK_TYPE, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), node)

    def test_ttt_empty(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_ttt_voided(self):
        text = (
            "This is **** with an __ word and a `` and an !["
            "](https://i.imgur.com/bsbWldj.jpeg) and a [](https://ttt.nowhere.net)"
        )
        node = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode(" with an ", TextType.PLAIN_TYPE),
            TextNode(" word and a ", TextType.PLAIN_TYPE),
            TextNode(" and an ", TextType.PLAIN_TYPE),
            TextNode("", TextType.IMAGE_TYPE, "https://i.imgur.com/bsbWldj.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TYPE),
        ]
        self.assertEqual(text_to_textnodes(text), node)
