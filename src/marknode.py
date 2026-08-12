from textnode import TextType, TextNode
import re

def split_nodes_delimiter(
	old_nodes: list[TextNode],
	delimiter: str,
	text_type: TextType
) -> list[TextNode]:
	marked = []
	for olnod in old_nodes:
		if olnod.text_type != TextType.PLAIN_TYPE:
			marked.append(olnod)
			continue
		if len(olnod.text.split(delimiter)) % 2 == 0:
			raise ValueError("invalid markdown syntax")
		parts = olnod.text.split(delimiter)
		nunods = []
		for n in range(0, len(parts)):
			if parts[n] == "":
				continue
			if n % 2 == 0:
				node = TextNode(
					parts[n],
					TextType.PLAIN_TYPE,
				)
				nunods.append(node)
			else:
				node = TextNode(
					parts[n],
					text_type,
				)
				nunods.append(node)
		marked.extend(nunods)
		continue
	return marked

def extract_markdown_images(text: str) -> list[tuple[str]]:
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str]]:
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
