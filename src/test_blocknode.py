import unittest
from blocknode import BlockType
from blocknode import markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis "
                "is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mtb_once(self):
        md = "There's only one paragraph."
        self.assertEqual(markdown_to_blocks(md), [md])

    def test_mtb_whitespace(self):
        md = """
	This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line	

- This is a list
- with items    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis "
                "is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mtb_null(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_mtb_holes(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis "
                "is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_btbt_base(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.BLOCK)

    def test_btbt_face(self):
        self.assertEqual(block_to_block_type("#### That, a heading."), BlockType.HEAD)

    def test_btbt_daze(self):
        block = """```
trigger = False
tik = float("-inf")
while True:
    if trigger:
        break
    if tik > 0:
        trigger = True
    tik += 10^10
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_btbt_sayz(self):
        block = """> This is a wise saying.
> Continued on the next line.
> And wrapped up here."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_btbt_pace(self):
        block = """- This is a wise saying.
- Continued on the next line.
- And wrapped up here."""
        self.assertEqual(block_to_block_type(block), BlockType.UNORD_LST)

    def test_btbt_case(self):
        block = """1. First step
2. Second step
3. Third step"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDER_LST)

    def test_btbt_mace(self):
        block = """> This is a wise saying.
 Continued on the next line.
> And wrapped up here."""
        self.assertEqual(block_to_block_type(block), BlockType.BLOCK)

    def test_btbt_vase(self):
        block = """- This is a wise saying.
- Continued on the next line.
 And wrapped up here."""
        self.assertEqual(block_to_block_type(block), BlockType.BLOCK)

    def test_btbt_lace(self):
        block = """1. First step
2. Second step
4. Third step"""
        self.assertEqual(block_to_block_type(block), BlockType.BLOCK)

    def test_btbt_fels(self):
        self.assertEqual(block_to_block_type(""), BlockType.BLOCK)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is "
            "another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** "
            "even with inline stuff\n</code></pre></div>",
        )

    def test_head_n_codlin(self):
        md = "#### This [button](fttp://Localhost:/Gate/bin) deletes system32!"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h4>This <a href="fttp://Localhost:/Gate/bin">button</a> '
            'deletes system32!</h4></div>',
        )

    def test_unord_bold(self):
        md = """
- You're **bald**
- I'm **thick**
- Just like ...
- **my dih** .. ner!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>You're <b>bald</b></li><li>I'm <b>thick</b></li><li>Just like "
            "...</li><li><b>my dih</b> .. ner!</li></ul></div>",
        )

    def test_ordr_12_coms(self):
        md = """
1. moomoo milk
2. giant eggs
3. aura cigs
4. P.P. elixirs
5. stamina potions
6. sword lube
7. suction arrows
8. heat shield
9. multi-venom antidotes
10. rubber repels
11. escape rope
12. monster alimony
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>moomoo milk</li><li>giant eggs</li><li>aura cigs</li><li>P.P. "
            "elixirs</li><li>stamina potions</li><li>sword lube</li><li>suction arrows</"
            "li><li>heat shield</li><li>multi-venom antidotes</li><li>rubber repels</li>"
            "<li>escape rope</li><li>monster alimony</li></ol></div>",
        )

    def test_quote_opt_ita(self):
        md = """
> I was reincarnated
> In _another world_
>now, my grossery lists preps me
>for _Monster-girls_ "hunting" !
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>I was reincarnated In <i>another world</i> now, my grossery "
            "lists preps me for <i>Monster-girls</i> \"hunting\" !</blockquote></div>",
        )

    def test_mxd_blocks(self):
        md = """
###### This [button](fttp://Localhost:/Gate/bin) deletes system32!

My name is Wiat Howtt and this is my story :

> I was reincarnated
> In **another world**
>now, my grossery lists preps me
>for _Monster-girls_ "hunting" !

Today is an other beautiful day!
Wow! Over here! What an exquisite specimen and that smooth mound...

- You're **bald**
- I'm **thick**
- Just like ...
- **my dih** .. ner!

`Narator: `In the heat of the ![>action<](https://imgflip.com/gif/8ba0x8)
our hero's satchel lets a revealing piece of paper slip out :

_HIS _**GROSSERY**_ LIST_

1. moomoo milk
2. giant eggs
3. aura cigs
4. P.P. elixirs
5. stamina potions
6. sword lube
7. suction arrows
8. heat shield
9. multi-venom antidotes
10. rubber repels
11. escape rope
12. monster alimony
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This <a href=\"fttp://Localhost:/Gate/bin\">button</a> "
            "deletes system32!</h6><p>My name is Wiat Howtt and this is my story :</p>"
            "<blockquote>I was reincarnated In <b>another world</b> now, my grossery "
            "lists preps me for <i>Monster-girls</i> \"hunting\" !</blockquote><p>"
            "Today is an other beautiful day! Wow! Over here! What an exquisite specimen"
            " and that smooth mound...</p><ul><li>You're <b>bald</b></li><li>I'm <b>"
            "thick</b></li><li>Just like ...</li><li><b>my dih</b> .. ner!</li></ul><p>"
            "<code>Narator: </code>In the heat of the <img src=\"https://imgflip.com/gif"
            "/8ba0x8\" alt=\">action<\"></img> our hero's satchel lets a revealing "
            "piece of paper slip out :</p><p><i>HIS </i><b>GROSSERY</b><i> LIST</i></p>"
            "<ol><li>moomoo milk</li><li>giant eggs</li><li>aura cigs</li><li>P.P. "
            "elixirs</li><li>stamina potions</li><li>sword lube</li><li>suction arrows</"
            "li><li>heat shield</li><li>multi-venom antidotes</li><li>rubber repels</li>"
            "<li>escape rope</li><li>monster alimony</li></ol></div>",
        )

    def test_heads_bound(self):
        md = """
# First : plow

## Second : sow

###Third : ?????

####### Profit!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First : plow</h1><h2>Second : sow</h2>"
            "<p>###Third : ?????</p><p>####### Profit!</p></div>",
        )

    def test_skip_ordr(self):
        md = """
### 

>


>
> 
>



1. 



- 
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>###</p><blockquote></blockquote><blockquote>  </blockquote><p>1.</p>"
            "<p>-</p></div>",
        )

    def test_void_block(self):
        self.assertEqual(markdown_to_html_node("").to_html(), "<div></div>")
