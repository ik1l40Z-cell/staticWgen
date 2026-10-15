from textnode import text_node_to_html_node, TextNode, TextType
from marknode import text_to_textnodes
from htmlnode import ParentNode
from enum import Enum
import re

def markdown_to_blocks(markdown):
	marked = []
	for block in markdown.split("\n\n"):
		blok = block.strip()
		if blok != "":
			marked.append(blok)
	return marked

class BlockType(Enum):
	BLOCK = "paragraph"
	HEAD = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORD_LST = "unordered_list"
	ORDER_LST = "ordered_list"

def block_to_block_type(md_block: str) -> "BlockType":
	hash = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
	validQ = True
	validU = True
	validO = True
	num = 1
	if md_block.startswith(hash):
		return BlockType.HEAD
	if md_block.startswith("```\n") and md_block.endswith("\n```"):
		return BlockType.CODE
	if md_block.startswith(">"):
		for lin in md_block.split("\n"):
			if not lin.startswith(">"):
				validQ = False
				break
		if validQ:
			return BlockType.QUOTE
	if md_block.startswith("- "):
		for lin in md_block.split("\n"):
			if not lin.startswith("- "):
				validU = False
				break
		if validU:
			return BlockType.UNORD_LST
	if md_block.startswith(f"{num}. "):
		for lin in md_block.split("\n"):
			if not lin.startswith(f"{num}. "):
				validO = False
				break
			num += 1
		if validO:
			return BlockType.ORDER_LST
	return BlockType.BLOCK

def count_block_hash(block: str) -> int:
	indx = 0
	while indx < len(block) and block[indx] == "#":
		indx += 1
	return indx

def list_items_tagged(block: str, type: "BlockType") -> list["LeafNode"]:
	tag_lst = []
	clean = ""
	for line in block.split("\n"):
		if type == BlockType.UNORD_LST:
			clean = line[2:]
		if type == BlockType.ORDER_LST:
			clean = re.sub(r"^\d+\.\s", "", line)
		tag_lst.append(ParentNode("li", text_to_children(clean)))
	return tag_lst

def strip_block_quote(block: str) -> str:
	strip = []
	for line in block.split("\n"):
		strip.append(re.sub(r"^\>\s*", "", line))
	return " ".join(strip)

def text_to_children(text: str) -> list["ParentNode"]:
	TxtLst = text_to_textnodes(text)
	HtmlLst = []
	for TxtNod in TxtLst:
		HtmlLst.append(text_node_to_html_node(TxtNod))
	return HtmlLst

def markdown_to_html_node(markdown: str) -> ParentNode:
	markblocks = markdown_to_blocks(markdown)
	Collectathon = []
	for block in markblocks:
		tag = None
		clean = ""
		type = block_to_block_type(block)
		if type == BlockType.BLOCK:
			tag = "p"
			strip = block.split("\n")
			clean = " ".join(strip)
		if type == BlockType.HEAD:
			num = count_block_hash(block)
			tag = f"h{num}"
			clean = block[num+1:]
		if type == BlockType.QUOTE:
			tag = "blockquote"
			clean = strip_block_quote(block)
		if tag is not None:
			HtmlNod = ParentNode(tag, text_to_children(clean))

		if type == BlockType.CODE:
			HtmlNod = ParentNode(
				"pre",
				[ParentNode(
					"code",
					[text_node_to_html_node(
						TextNode(
							block[4:-3],
							TextType.PLAIN_TYPE,
						),
					)],
				)],
			)
		if type == BlockType.UNORD_LST:
			HtmlNod = ParentNode("ul", list_items_tagged(block, type))
		if type == BlockType.ORDER_LST:
			HtmlNod = ParentNode("ol", list_items_tagged(block, type))

		Collectathon.append(HtmlNod)
	return ParentNode("div", Collectathon)
