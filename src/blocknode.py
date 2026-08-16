
def markdown_to_blocks(markdown):
	marked = []
	for block in markdown.split("\n\n"):
		blok = block.strip()
		if blok != "":
			marked.append(blok)
	return marked
