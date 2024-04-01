class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError
        prop_html = ""
        if self.props != None:
            for prop in self.props:
                prop_html = f'{prop_html} {prop}="{self.props[prop]}"'
        if self.tag == None:
            return self.value
        return f"<{self.tag}{prop_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if self.tag == None:
            return ValueError("Missing tag")
        if self.children == None:
            return ValueError("Missing children")
        prop_html = ""
        if self.props != None:
            for prop in self.props:
                prop_html = f'{prop_html} {prop}="{self.props[prop]}"'
        return f"<{self.tag}{prop_html}>{"".join(list(map(lambda x: x.to_html(), self.children)))}</{self.tag}>"