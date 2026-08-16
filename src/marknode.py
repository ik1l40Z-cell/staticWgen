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

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
	marked = []
	for olnod in old_nodes:
		if olnod.text_type == TextType.IMAGE_TYPE:
			marked.append(olnod)
			continue
		parts = extract_markdown_images(olnod.text)
		if parts == []:
			marked.append(olnod)
			continue
		nunods = []
		undods = []
		to_split = olnod.text
		for prt in parts:
			node = TextNode(
				prt[0],
				TextType.IMAGE_TYPE,
				prt[1],
			)
			nunods.append(node)
			splat, to_split = to_split.split(f"![{prt[0]}]({prt[1]})", 1)
			undods.append(TextNode(splat, TextType.PLAIN_TYPE))
			if extract_markdown_images(to_split) == []:
				undods.append(TextNode(to_split, TextType.PLAIN_TYPE))
		for dex in range(len(nunods)):
			if undods[dex].text != "":
				marked.append(undods[dex])
			if nunods[dex].url != "":
				marked.append(nunods[dex])
		if len(undods) > 1 and undods[-1].text != "":
			marked.append(undods[-1])
	return marked

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
	marked = []
	for olnod in old_nodes:
		if olnod.text_type == TextType.LINK_TYPE:
			marked.append(olnod)
			continue
		parts = extract_markdown_links(olnod.text)
		if parts == []:
			marked.append(olnod)
			continue
		nunods = []
		undods = []
		to_split = olnod.text
		for prt in parts:
			node = TextNode(
				prt[0],
				TextType.LINK_TYPE,
				prt[1],
			)
			nunods.append(node)
			splat, to_split = to_split.split(f"[{prt[0]}]({prt[1]})", 1)
			undods.append(TextNode(splat, TextType.PLAIN_TYPE))
			if extract_markdown_links(to_split) == []:
                                undods.append(TextNode(to_split, TextType.PLAIN_TYPE))
		for dex in range(len(nunods)):
			if undods[dex].text != "":
				marked.append(undods[dex])
			if nunods[dex].url != "" and nunods[dex].text != "":
				marked.append(nunods[dex])
		if len(undods) > 1 and undods[-1].text != "":
			marked.append(undods[-1])
	return marked

def text_to_textnodes(text: str) -> list[TextNode]:
	init_node = [TextNode(text, TextType.PLAIN_TYPE)]
	bold_nods = split_nodes_delimiter(init_node, "**", TextType.BOLD_TYPE)
	ital_nods = split_nodes_delimiter(bold_nods, "_", TextType.ITALIC_TYPE)
	code_nods = split_nodes_delimiter(ital_nods, "`", TextType.CODE_TYPE)
	imag_nods = split_nodes_images(code_nods)
	link_nods = split_nodes_links(imag_nods)
	return link_nods
