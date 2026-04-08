from __future__ import annotations

from html import escape as html_escape

from docutils import nodes
from docutils.parsers.rst import Directive, directives

class SageCellDirective(Directive):
    has_content = True
    option_spec = {
        "server": directives.unchanged,
        "autoeval": directives.flag,
    }

    def run(self):
        code = "\n".join(self.content).rstrip("\n")
        server = (self.options.get("server") or "https://sagecell.sagemath.org").rstrip("/")
        autoeval = "true" if "autoeval" in self.options else "false"

        html = (
            f'<div class="sagecell" data-sagecell-server="{server}" '
            f'data-sagecell-autoeval="{autoeval}">'
            f'<textarea class="sagecell-input" rows="8" cols="80">{html_escape(code)}</textarea>'
            f'<div class="sagecell-output"></div>'
            f"</div>"
        )
        return [nodes.raw("", html, format="html")]

def setup(app):
    app.add_directive("sagecell", SageCellDirective)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
