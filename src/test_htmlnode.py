import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_ceq(self):
        child = HTMLNode("p", "Do you know the way ?")
        parent = HTMLNode("a", None, [child], {"href": "https://www.google.com"})
        self.assertEqual(parent.child, [child])

    def test_rs(self):
        node = HTMLNode("p", "Do you know the way ?")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_no(self):
        node = HTMLNode("a", "Do you know the way ?", None)
        self.assertIsNone(node.child)

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
        self.assertIsNone(node.child)

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

    def test_to_html_with_child(self):
        child = LeafNode("span", "daughter ?")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>daughter ?</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild = LeafNode("b", "barely spoilled her !")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>barely spoilled her !</b></span></div>",
        )

    def test_to_html_with_void(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), '<div></div>')

    def test_to_html_with_props(self):
        child = LeafNode("span", "dot her ?", {"am": "_a", "href": "https://www.brokeboy.com"})
        parent = ParentNode("div", [child], {"bank": "_empty", "with": "_this.economy?"})
        self.assertEqual(parent.to_html(), '<div bank="_empty" with="_this.economy?"><span am="_a" href="https://www.brokeboy.com">dot her ?</span></div>')

    def test_to_html_with_bigF(self):
        youngest = LeafNode("b", "held her,")
        secnd_yngst = LeafNode("span", " fed her,")
        middle_one = LeafNode("a", " spoilled her,")
        secnd_oldst = LeafNode("i", " taught her,")
        oldest = LeafNode("p", " sent her.")
        parent = ParentNode("div", [youngest, secnd_yngst, middle_one, secnd_oldst, oldest])
        self.assertEqual(
            parent.to_html(),
            "<div><b>held her,</b><span> fed her,</span><a> spoilled her,</a><i> taught her,</i><p> sent her.</p></div>",
        )

    def test_to_html_with_plane(self):
        child = LeafNode(None, "Flyer ?")
        niece = LeafNode(None, " barely launched her !")
        aunt = ParentNode("a", [niece])
        parent = ParentNode("b", [child, aunt])
        self.assertEqual(parent.to_html(), "<b>Flyer ?<a> barely launched her !</a></b>")

    def test_to_html_with_Funit(self):
        lil_sis = LeafNode("span", "Sailor ?")
        big_sis = LeafNode("div", " barely baught her !")
        niece = ParentNode("em", [lil_sis])
        aunt = ParentNode("a", [niece])
        parent = ParentNode("b", [aunt, big_sis])
        self.assertEqual(parent.to_html(), "<b><a><em><span>Sailor ?</span></em></a><div> barely baught her !</div></b>")

    def test_to_html_with_tree(self):
        baby = LeafNode("b", " an other ?")
        mother = ParentNode("b", [baby])
        baby_sis = LeafNode("i", " ready for")
        father = ParentNode("p", [baby_sis, mother])
        neice = LeafNode(None, " we are")
        sis = LeafNode("a", " we know")
        unc = ParentNode("em", [neice])
        grandma = ParentNode("sq", [sis])
        big_sis = LeafNode(None, " will we")
        great_unc = LeafNode("h1", "Ma' Pa' ! When")
        great_aunt = ParentNode("h2", [big_sis])
        tree = [great_unc, great_aunt, grandma, unc, father]
        grandpa = ParentNode("div", tree)
        delivery = "<div><h1>Ma' Pa' ! When</h1><h2> will we</h2><sq><a> we know</a></sq><em> we are</em><p><i> ready for</i><b><b> an other ?</b></b></p></div>"
        self.assertEqual(grandpa.to_html(), delivery)

    def test_to_html_without_tag(self):
        naught = LeafNode(None, "if u no dot, u get a naughter", {"sign": "_made.up"})
        node = ParentNode(None, [naught], {"borg": "ai_"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_child(self):
        node = ParentNode("b", None, {"when": "_no.dot", "get": "_naughter", "borg": "ai_"})
        with self.assertRaises(ValueError):
            node.to_html()
