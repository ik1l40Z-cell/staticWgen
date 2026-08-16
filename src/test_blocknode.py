import unittest
from blocknode import markdown_to_blocks

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
