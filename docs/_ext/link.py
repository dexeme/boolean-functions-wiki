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
    node = nodes.raw('', html_code, format='html')

    return [node], []


def zotero_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    if options is None:
        options = {}

    if '<' in text and '>' in text:
        parts = text.rsplit('<', 1)
        display_text = parts[0].strip()
        item_key = parts[1].rstrip('>').strip()
    else:
        display_text = text
        item_key = text

    uri = f"zotero://select/library/items/{item_key}"
    node = nodes.reference(rawtext, display_text, refuri=uri)

    return [node], []


def setup(app):
    app.add_role('link', link_role)
    app.add_role('zotero', zotero_role)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }