class HTMLNode:
	def __init__(
		self,
		tag: str | None = None,
		value: str | None = None,
		child: list["HTMLNode"] | None = None,
		props: dict[str, str] | None = None,
	):
		self.tag = tag
		self.value = value
		self.child = child
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
		return f"{self.tag} {self.value} {self.child} {self.props}"


class LeafNode(HTMLNode):
	def __init__(
		self,
		tag: str | None,
		value: str,
		props: dict[str, str] | None = None,
	):
		super().__init__(tag, value, child=None, props=props)

	def to_html(self) -> str:
		if not self.value:
			raise ValueError("no text to print")
		if self.tag is None:
			return self.value
		made = self.props_to_html()
		return f"<{self.tag}{made}>{self.value}</{self.tag}>"

	def __repr__(self) -> str:
		return f"{self.tag} {self.value} {self.props}"


class ParentNode(HTMLNode):
	def __init__(
		self,
		tag: str,
		child: list["HTMLNode"],
		props: dict[str, str] | None = None,
	):
		super().__init__(tag, value=None, child=child, props=props)

	def to_html(self) -> str:
		if self.tag is None:
			raise ValueError("need for marker")
		if self.child is None:
			raise ValueError("missing children")
		create = ""
		made = self.props_to_html()
		for chi in self.child:
			create += chi.to_html()
		return f"<{self.tag}{made}>{create}</{self.tag}>"
