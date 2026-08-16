from enum import Enum

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
