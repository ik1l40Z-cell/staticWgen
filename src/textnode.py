from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	PLAIN_TYPE = "plain"
	BOLD_TYPE = "bold"
	ITALIC_TYPE = "italic"
	CODE_TYPE = "code"
	LINK_TYPE = "link"
	IMAGE_TYPE = "image"


class TextNode:
	def __init__(self, text: str, text_type: TextType, url: str | None = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: "TextNode") -> "LeafNode":
	if text_node.text_type == TextType.PLAIN_TYPE:
		return LeafNode(None, text_node.text)
	if text_node.text_type == TextType.BOLD_TYPE:
		return LeafNode("b", text_node.text)
	if text_node.text_type == TextType.ITALIC_TYPE:
		return LeafNode("i", text_node.text)
	if text_node.text_type == TextType.CODE_TYPE:
		return LeafNode("code", text_node.text)
	if text_node.text_type == TextType.LINK_TYPE:
		return LeafNode("a", text_node.text, {"href": text_node.url})
	if text_node.text_type == TextType.IMAGE_TYPE:
		return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
	raise Exception()
