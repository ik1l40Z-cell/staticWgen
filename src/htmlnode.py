class HTMLNode:
	def __init__(
		self,
		tag: str | None = None,
		value: str | None = None,
		children: list["HTMLNode"] | None = None,
		props: dict[str, str] | None = None,
	):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self) -> str:
		if not self.props:
			return ""
		prop = ""
		for key, val in self.props.items():
			prop += f' {key}="{val}"'
		return prop

	def __repr__(self) -> str:
		return f"{self.tag} {self.value} {self.children} {self.props}"


class LeafNode(HTMLNode):
	def __init__(
		self,
		tag: str | None,
		value: str,
		props: dict[str, str] | None = None,
	):
		super().__init__(tag, value, children=None, props=props)

	def to_html(self) -> str:
		if not self.value:
			raise ValueError("no text to print")
		if self.tag is None:
			return self.value
		made = self.props_to_html()
		return f"<{self.tag}{made}>{self.value}</{self.tag}>"

	def __repr__(self) -> str:
		return f"{self.tag} {self.value} {self.props}"
