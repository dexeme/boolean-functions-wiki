from docutils import nodes

def link_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    if options is None:
        options = {}

    if '<' in text and '>' in text:
        parts = text.rsplit('<', 1)
        display_text = parts[0].strip()
        url = parts[1].rstrip('>').strip()
    else:
        display_text = text
        url = text

    html_code = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{display_text}</a>'
    raw_node = nodes.raw('', html_code, format='html')

    return [raw_node], []

def setup(app):
    app.add_role('link', link_role)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
