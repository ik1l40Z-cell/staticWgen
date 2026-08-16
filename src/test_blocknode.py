import unittest
from blocknode import markdown_to_blocks, BlockType, block_to_block_type

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
