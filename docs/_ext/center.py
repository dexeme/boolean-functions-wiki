from docutils import nodes
from docutils.parsers.rst import Directive


class CenterDirective(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        text = self.arguments[0].strip()
        container = nodes.container(classes=["bf-center"])
        paragraph = nodes.paragraph()
        inline_nodes, messages = self.state.inline_text(text, self.lineno)
        paragraph.extend(inline_nodes)
        container += paragraph
        return [container, *messages]


def setup(app):
    app.add_directive("center", CenterDirective)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
