from textnode import TextNode, TextType

def main():
	output_one = TextNode("dummy thicc lab-bear", TextType.BOLD_TYPE, None)
	output_two = TextNode("Aim for the code-lord", TextType.LINK_TYPE, "https://www.boot.dev")
	print(output_one)
	print(output_two)

if __name__ == "__main__":
	main()
