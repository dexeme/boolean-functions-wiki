from docutils.parsers.rst.directives.body import CodeBlock

class SageBlock(CodeBlock):
    def run(self):
        if not self.arguments:
            self.arguments = ["python"]
        self.options.setdefault("class", []).append("sage")
        return super().run()

def setup(app):
    app.add_directive("sage", SageBlock)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}