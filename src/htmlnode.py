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

	def props_to_html(self):
		if not self.props:
			return ""
		prop = ""
		for key, val in self.props.items():
			prop += f' {key}="{val}"'
		return prop

	def __repr__(self):
		return f"{self.tag} {self.value} {self.children} {self.props}"
