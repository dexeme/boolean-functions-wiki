from __future__ import annotations

from html import escape as html_escape
from pathlib import Path
import re

from docutils import nodes
from docutils.parsers.rst import Directive


class LazyChunksDirective(Directive):
    has_content = True
    _RANGE_RE = re.compile(r"^(\d+)_(\d+)$")

    def _discover_tree_from_folder(
        self, folder_name: str
    ) -> list[tuple[int, int, list[tuple[int, int]]]]:
        env = self.state.document.settings.env
        src_dir = Path(env.app.srcdir)
        base = src_dir / "content" / "_includes" / folder_name
        if not base.exists() or not base.is_dir():
            raise self.error(
                f"Auto lazychunks folder not found: content/_includes/{folder_name}"
            )

        intervals: list[tuple[int, int, list[tuple[int, int]]]] = []
        for child in base.iterdir():
            if not child.is_dir():
                continue
            m = self._RANGE_RE.fullmatch(child.name)
            if not m:
                continue
            a, b = map(int, m.groups())
            subintervals: list[tuple[int, int]] = []
            for sub in child.iterdir():
                if not sub.is_file() or sub.suffix != ".rst":
                    continue
                sm = self._RANGE_RE.fullmatch(sub.stem)
                if not sm:
                    continue
                sa, sb = map(int, sm.groups())
                subintervals.append((sa, sb))
            subintervals.sort()
            intervals.append((a, b, subintervals))

        if not intervals:
            raise self.error(
                f"No interval subfolders found in content/_includes/{folder_name}"
            )

        intervals.sort()
        return intervals

    def run(self):
        if not self.content:
            return []

        items = [
            line.strip()
            for line in self.content
            if line.strip() and not line.strip().startswith("#")
        ]
        if not items:
            return []

        auto_tree: list[tuple[int, int, list[tuple[int, int]]]] | None = None
        # Auto mode: provide only the folder name under content/_includes.
        if len(items) == 1 and "|" not in items[0]:
            folder_name = items[0]
            auto_tree = self._discover_tree_from_folder(folder_name)
        else:
            entries: list[tuple[str, str]] = []
            for item in items:
                if "|" not in item:
                    raise self.error(
                        "Each line must be 'label | src', or provide a single folder name for auto mode."
                    )
                label, src = [part.strip() for part in item.split("|", 1)]
                if not label or not src:
                    raise self.error("Each line must provide both label and src.")
                entries.append((label, src))

        serial = self.state.document.settings.env.new_serialno("lazychunks")
        wrapper_id = f"lazychunks-{serial}"

        parts = [f'<div id="{wrapper_id}" class="lazychunks">']
        if auto_tree is not None:
            for a, b, subintervals in auto_tree:
                parts.append(
                    '<details class="apn-range-chunk">'
                    "<summary><strong>{}</strong></summary>".format(
                        html_escape(f"IDs {a}-{b}")
                    )
                )
                parts.append('<div class="lazychunks lazychunks-sub">')
                if subintervals:
                    for sa, sb in subintervals:
                        src = f"../_static/apn_chunks/{folder_name}_{sa}_{sb}.html"
                        parts.append(
                            '<details class="apn-lazy-chunk" data-src="{}">'
                            '<summary><strong>{}</strong></summary>'
                            '<div class="apn-lazy-body"></div>'
                            "</details>".format(
                                html_escape(src, quote=True),
                                html_escape(f"IDs {sa}-{sb}"),
                            )
                        )
                else:
                    src = f"../_static/apn_chunks/{folder_name}_{a}_{b}.html"
                    parts.append(
                        '<details class="apn-lazy-chunk" data-src="{}">'
                        '<summary><strong>{}</strong></summary>'
                        '<div class="apn-lazy-body"></div>'
                        "</details>".format(
                            html_escape(src, quote=True),
                            html_escape(f"IDs {a}-{b}"),
                        )
                    )
                parts.append("</div>")
                parts.append("</details>")
        else:
            for label, src in entries:
                parts.append(
                    '<details class="apn-lazy-chunk" data-src="{}">'
                    '<summary><strong>{}</strong></summary>'
                    '<div class="apn-lazy-body"></div>'
                    "</details>".format(html_escape(src, quote=True), html_escape(label))
                )
        parts.append("</div>")
        parts.append("<script>")
        parts.append("(function () {")
        parts.append("  if (window.__lazyChunksBound !== true) {")
        parts.append("    window.__lazyChunksBound = true;")
        parts.append("    document.addEventListener('toggle', async function (event) {")
        parts.append("      const chunk = event.target;")
        parts.append("      if (!(chunk instanceof HTMLDetailsElement)) return;")
        parts.append("      if (!chunk.classList.contains('apn-lazy-chunk')) return;")
        parts.append("      if (!chunk.open || chunk.dataset.loaded === '1') return;")
        parts.append("      const body = chunk.querySelector('.apn-lazy-body');")
        parts.append("      const src = chunk.dataset.src;")
        parts.append("      if (!body || !src) return;")
        parts.append("      body.textContent = 'Loading...';")
        parts.append("      try {")
        parts.append("        const response = await fetch(src);")
        parts.append("        if (!response.ok) throw new Error('HTTP ' + response.status);")
        parts.append("        body.innerHTML = await response.text();")
        parts.append("        chunk.dataset.loaded = '1';")
        parts.append("      } catch (err) {")
        parts.append("        body.innerHTML = '';")
        parts.append("        const frame = document.createElement('iframe');")
        parts.append("        frame.src = src;")
        parts.append("        frame.loading = 'lazy';")
        parts.append("        frame.style.width = '100%';")
        parts.append("        frame.style.minHeight = '600px';")
        parts.append("        frame.style.border = '1px solid #ccc';")
        parts.append("        body.appendChild(frame);")
        parts.append("        chunk.dataset.loaded = '1';")
        parts.append("      }")
        parts.append("    }, true);")
        parts.append("  }")
        parts.append("})();")
        parts.append("</script>")

        html = "\n".join(parts)
        return [nodes.raw("", html, format="html")]


def setup(app):
    app.add_directive("lazychunks", LazyChunksDirective)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
