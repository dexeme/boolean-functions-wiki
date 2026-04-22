from __future__ import annotations

import csv
from html import escape as html_escape
from pathlib import Path
import re

from docutils import nodes
from docutils.parsers.rst import Directive, directives


_CHUNK_MATHJAX_BOOTSTRAP = """
<script>
(function () {
  function renderWithParentMathJax() {
    try {
      if (!window.parent || window.parent === window) return false;
      const pmj = window.parent.MathJax;
      if (!pmj || typeof pmj.tex2chtml !== 'function') return false;
      const nodes = document.querySelectorAll('span.math.notranslate.nohighlight');
      for (const node of nodes) {
        const source = (node.textContent || '').trim();
        const m = source.match(/^\\\\\\((.*)\\\\\\)$/s);
        if (!m) continue;
        const rendered = pmj.tex2chtml(m[1], { display: false });
        node.textContent = '';
        node.appendChild(document.importNode(rendered, true));
      }
      return true;
    } catch (_err) {
      return false;
    }
  }

  async function ensureMathJaxAndTypeset() {
    if (renderWithParentMathJax()) return;

    const tryTypeset = async () => {
      if (!window.MathJax) return false;
      try {
        if (window.MathJax.startup && window.MathJax.startup.promise) {
          await window.MathJax.startup.promise;
        }
        if (typeof window.MathJax.typesetPromise === 'function') {
          await window.MathJax.typesetPromise([document.body]);
          return true;
        }
        if (window.MathJax.Hub && typeof window.MathJax.Hub.Queue === 'function') {
          window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, document.body]);
          return true;
        }
      } catch (_err) {
      }
      return false;
    };

    if (await tryTypeset()) return;

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
    script.async = true;
    script.onload = async () => { await tryTypeset(); };
    document.head.appendChild(script);
  }

  ensureMathJaxAndTypeset();
})();
</script>
""".strip()

def _read_csv_table(csv_path: Path) -> tuple[list[str], list[list[str]]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [], []
    return [c.strip() for c in rows[0]], [[c.strip() for c in row] for row in rows[1:]]


def _cell_html(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        inner_math = text[1:-1].strip()
        return '<span class="math notranslate nohighlight">\\({}\\)</span>'.format(
            html_escape(inner_math)
        )
    if len(text) >= 2 and text[0] == "$" and text[-1] == "$":
        inner_math = text[1:-1].strip()
        return '<span class="math notranslate nohighlight">\\({}\\)</span>'.format(
            html_escape(inner_math)
        )
    if text.startswith("\\(") and text.endswith("\\)"):
        inner_math = text[2:-2].strip()
        return '<span class="math notranslate nohighlight">\\({}\\)</span>'.format(
            html_escape(inner_math)
        )
    return html_escape(text)


def _csv_rows_to_html(header: list[str], rows: list[list[str]]) -> str | None:
    if not header:
        return None
    parts = ['<table class="docutils align-default">', "<thead><tr>"]
    for col in header:
        parts.append("<th>{}</th>".format(_cell_html(col)))
    parts.extend(["</tr></thead>", "<tbody>"])
    width = len(header)
    for row in rows:
        normalized = list(row[:width]) + [""] * max(0, width - len(row))
        parts.append("<tr>")
        for cell in normalized:
            parts.append("<td>{}</td>".format(_cell_html(cell)))
        parts.append("</tr>")
    parts.extend(["</tbody>", "</table>"])
    parts.append(_CHUNK_MATHJAX_BOOTSTRAP)
    return "\n".join(parts) + "\n"


def _parse_lazychunks_blocks(rst_text: str) -> list[tuple[dict[str, str], list[str]]]:
    blocks: list[tuple[dict[str, str], list[str]]] = []
    lines = rst_text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() != ".. lazychunks::":
            i += 1
            continue
        i += 1
        options: dict[str, str] = {}
        content: list[str] = []
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                continue
            if not line.startswith((" ", "\t")):
                break
            opt = re.match(r"\s*:([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
            if opt:
                options[opt.group(1)] = opt.group(2)
            elif not stripped.startswith("#"):
                content.append(stripped)
            i += 1
        blocks.append((options, content))
    return blocks


def _resolve_csv_path(src_dir: Path, value: str) -> Path:
    rel = Path(value)
    candidates = [
        src_dir / "content" / "tables" / rel,
        src_dir / "tables" / rel,
        src_dir / "content" / rel,
        src_dir / "pages" / rel,
        src_dir / rel,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def _resolve_includes_base(src_dir: Path, folder_name: str) -> Path:
    candidates = [
        src_dir / "content" / "_includes" / folder_name,
        src_dir / "_includes" / folder_name,
        src_dir / "pages" / "_includes" / folder_name,
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return candidates[0]


def _csv_chunk_meta(rows: list[list[str]], max_rows: int) -> list[tuple[int, int, str, str]]:
    chunks: list[tuple[int, int, str, str]] = []
    if max_rows <= 0:
        return chunks
    total = len(rows)
    for idx in range(0, total, max_rows):
        chunk_rows = rows[idx:idx + max_rows]
        start = idx + 1
        end = idx + len(chunk_rows)
        first_id = chunk_rows[0][0].strip() if chunk_rows and chunk_rows[0] else str(start)
        last_id = chunk_rows[-1][0].strip() if chunk_rows and chunk_rows[-1] else str(end)
        chunks.append((start, end, first_id, last_id))
    return chunks


class LazyChunksDirective(Directive):
    has_content = True
    option_spec = {
        "csv": directives.path,
        "max-rows": directives.positive_int,
    }
    _RANGE_RE = re.compile(r"^(\d+)_(\d+)$")

    @staticmethod
    def _append_mathjax_retypeset(parts: list[str], scope_expr: str) -> None:
        parts.append("        for (let i = 0; i < 20; i += 1) {")
        parts.append("          const mj = window.MathJax;")
        parts.append("          if (!mj) {")
        parts.append("            await new Promise((resolve) => setTimeout(resolve, 150));")
        parts.append("            continue;")
        parts.append("          }")
        parts.append("          try {")
        parts.append("            if (mj.startup && mj.startup.promise) {")
        parts.append("              await mj.startup.promise;")
        parts.append("            }")
        parts.append("            if (typeof mj.typesetPromise === 'function') {")
        parts.append(f"              await mj.typesetPromise([{scope_expr}]);")
        parts.append("              break;")
        parts.append("            }")
        parts.append("            if (mj.Hub && typeof mj.Hub.Queue === 'function') {")
        parts.append(f"              mj.Hub.Queue(['Typeset', mj.Hub, {scope_expr}]);")
        parts.append("              break;")
        parts.append("            }")
        parts.append("          } catch (_err) {")
        parts.append("            // Retry below.")
        parts.append("          }")
        parts.append("          await new Promise((resolve) => setTimeout(resolve, 150));")
        parts.append("        }")

    def _discover_tree_from_folder(
        self, folder_name: str
    ) -> list[tuple[int, int, list[tuple[int, int]]]]:
        env = self.state.document.settings.env
        src_dir = Path(env.app.srcdir)
        base = _resolve_includes_base(src_dir, folder_name)
        if not base.exists() or not base.is_dir():
            raise self.error(
                "Auto lazychunks folder not found in any of: "
                f"content/_includes/{folder_name}, _includes/{folder_name}, "
                f"pages/_includes/{folder_name}"
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
                "No interval subfolders found in: "
                f"{base}"
            )

        intervals.sort()
        return intervals

    def run(self):
        if not self.content:
            if "csv" not in self.options:
                return []

        items = [
            line.strip()
            for line in self.content
            if line.strip() and not line.strip().startswith("#")
        ]
        if not items and "csv" not in self.options:
            return []

        auto_tree: list[tuple[int, int, list[tuple[int, int]]]] | None = None
        csv_mode = "csv" in self.options
        csv_dataset = ""
        csv_chunks: list[tuple[int, int, str, str]] = []

        if csv_mode:
            env = self.state.document.settings.env
            src_dir = Path(env.app.srcdir)
            csv_path = _resolve_csv_path(src_dir, self.options["csv"])
            if not csv_path.is_file():
                raise self.error(
                    f"CSV file not found for lazychunks: {self.options['csv']}"
                )
            max_rows = self.options.get("max-rows", 100)
            if items:
                csv_dataset = items[0]
            else:
                csv_dataset = Path(self.options["csv"]).stem
            _, csv_rows = _read_csv_table(csv_path)
            csv_chunks = _csv_chunk_meta(csv_rows, max_rows)
            if not csv_chunks:
                raise self.error(f"CSV has no data rows: {csv_path}")
        # Auto mode: provide only the folder name under content/_includes.
        elif len(items) == 1 and "|" not in items[0]:
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
        if csv_mode:
            for start, end, first_id, last_id in csv_chunks:
                src = f"{csv_dataset}_{start}_{end}.html"
                parts.append(
                    '<details class="apn-lazy-chunk" data-src="{}" data-src-kind="apn-chunk">'
                    '<summary><strong>{}</strong></summary>'
                    '<div class="apn-lazy-body"></div>'
                    "</details>".format(
                        html_escape(src, quote=True),
                        html_escape(f"IDs {first_id}-{last_id}"),
                    )
                )
        elif auto_tree is not None:
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
                        src = f"{folder_name}_{sa}_{sb}.html"
                        parts.append(
                            '<details class="apn-lazy-chunk" data-src="{}" data-src-kind="apn-chunk">'
                            '<summary><strong>{}</strong></summary>'
                            '<div class="apn-lazy-body"></div>'
                            "</details>".format(
                                html_escape(src, quote=True),
                                html_escape(f"IDs {sa}-{sb}"),
                            )
                        )
                else:
                    src = f"{folder_name}_{a}_{b}.html"
                    parts.append(
                        '<details class="apn-lazy-chunk" data-src="{}" data-src-kind="apn-chunk">'
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
        parts.append("    if (typeof window.__lazyChunksQueueTypeset !== 'function') {")
        parts.append("      window.__lazyChunksPendingTypeset = new Set();")
        parts.append("      window.__lazyChunksTryTypeset = async function (el) {")
        parts.append("        if (!el || !document.contains(el)) return true;")
        parts.append("        const mj = window.MathJax;")
        parts.append("        if (!mj) return false;")
        parts.append("        try {")
        parts.append("          if (mj.startup && mj.startup.promise) {")
        parts.append("            await mj.startup.promise;")
        parts.append("          }")
        parts.append("          if (typeof mj.typesetPromise === 'function') {")
        parts.append("            await mj.typesetPromise([el]);")
        parts.append("            return true;")
        parts.append("          }")
        parts.append("          if (mj.Hub && typeof mj.Hub.Queue === 'function') {")
        parts.append("            mj.Hub.Queue(['Typeset', mj.Hub, el]);")
        parts.append("            return true;")
        parts.append("          }")
        parts.append("        } catch (_err) {")
        parts.append("          return false;")
        parts.append("        }")
        parts.append("        return false;")
        parts.append("      };")
        parts.append("      window.__lazyChunksFlushTypeset = async function () {")
        parts.append("        const pending = Array.from(window.__lazyChunksPendingTypeset);")
        parts.append("        for (const el of pending) {")
        parts.append("          const ok = await window.__lazyChunksTryTypeset(el);")
        parts.append("          if (ok) window.__lazyChunksPendingTypeset.delete(el);")
        parts.append("        }")
        parts.append("        if (window.__lazyChunksPendingTypeset.size === 0 && window.__lazyChunksTypesetTimer) {")
        parts.append("          clearInterval(window.__lazyChunksTypesetTimer);")
        parts.append("          window.__lazyChunksTypesetTimer = null;")
        parts.append("        }")
        parts.append("      };")
        parts.append("      window.__lazyChunksQueueTypeset = function (el) {")
        parts.append("        if (!el) return;")
        parts.append("        window.__lazyChunksPendingTypeset.add(el);")
        parts.append("        void window.__lazyChunksFlushTypeset();")
        parts.append("        if (!window.__lazyChunksTypesetTimer) {")
        parts.append("          window.__lazyChunksTypesetTimer = setInterval(function () {")
        parts.append("            void window.__lazyChunksFlushTypeset();")
        parts.append("          }, 300);")
        parts.append("        }")
        parts.append("      };")
        parts.append("    }")
        parts.append("    const lazyChunksUseIframeOnly = window.location.protocol === 'file:';")
        parts.append("    const lazyChunksContentRoot = (document.documentElement && document.documentElement.getAttribute('data-content_root')) || '';")
        parts.append("    const lazyChunksResolveSrc = function (chunk, src) {")
        parts.append("      if (!src) return src;")
        parts.append("      if (chunk.dataset.srcKind !== 'apn-chunk') return src;")
        parts.append("      let root = lazyChunksContentRoot;")
        parts.append("      if (!root && typeof DOCUMENTATION_OPTIONS !== 'undefined' && DOCUMENTATION_OPTIONS && DOCUMENTATION_OPTIONS.URL_ROOT) {")
        parts.append("        root = DOCUMENTATION_OPTIONS.URL_ROOT;")
        parts.append("      }")
        parts.append("      const normalizedRoot = root && !root.endsWith('/') ? root + '/' : root;")
        parts.append("      return normalizedRoot + '_static/apn_chunks/' + src;")
        parts.append("    };")
        parts.append("    const lazyChunksLoadIframe = function (body, src, chunk) {")
        parts.append("      body.innerHTML = '';")
        parts.append("      const frame = document.createElement('iframe');")
        parts.append("      frame.src = src;")
        parts.append("      frame.loading = 'lazy';")
        parts.append("      frame.style.width = '100%';")
        parts.append("      frame.style.minHeight = '600px';")
        parts.append("      frame.style.border = '1px solid #ccc';")
        parts.append("      body.appendChild(frame);")
        parts.append("      chunk.dataset.loaded = '1';")
        parts.append("    };")
        parts.append("    document.addEventListener('toggle', async function (event) {")
        parts.append("      const chunk = event.target;")
        parts.append("      if (!(chunk instanceof HTMLDetailsElement)) return;")
        parts.append("      if (!chunk.classList.contains('apn-lazy-chunk')) return;")
        parts.append("      if (!chunk.open || chunk.dataset.loaded === '1') return;")
        parts.append("      const body = chunk.querySelector('.apn-lazy-body');")
        parts.append("      const rawSrc = chunk.dataset.src;")
        parts.append("      if (!body || !rawSrc) return;")
        parts.append("      const src = lazyChunksResolveSrc(chunk, rawSrc);")
        parts.append("      body.textContent = 'Loading...';")
        parts.append("      if (lazyChunksUseIframeOnly) {")
        parts.append("        lazyChunksLoadIframe(body, src, chunk);")
        parts.append("        return;")
        parts.append("      }")
        parts.append("      try {")
        parts.append("        const response = await fetch(src);")
        parts.append("        if (!response.ok) throw new Error('HTTP ' + response.status);")
        parts.append("        body.innerHTML = await response.text();")
        parts.append("        window.__lazyChunksQueueTypeset(body);")
        parts.append("        chunk.dataset.loaded = '1';")
        parts.append("      } catch (err) {")
        parts.append("        lazyChunksLoadIframe(body, src, chunk);")
        parts.append("      }")
        parts.append("    }, true);")
        parts.append("  }")
        parts.append("})();")
        parts.append("</script>")

        html = "\n".join(parts)
        return [nodes.raw("", html, format="html")]


def _parse_list_table_rows(rst_text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    lines = rst_text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"\s*\* -\s*(.+)\s*$", lines[i])
        if not m:
            i += 1
            continue
        c1 = m.group(1).strip()
        c2 = ""
        if i + 1 < len(lines):
            m2 = re.match(r"\s*-\s*(.+)\s*$", lines[i + 1])
            if m2:
                c2 = m2.group(1).strip()
                i += 1
        rows.append((c1, c2))
        i += 1
    return rows


def _list_table_rst_to_html(rst_text: str) -> str | None:
    rows = _parse_list_table_rows(rst_text)
    if len(rows) < 2:
        return None

    header = rows[0]
    body = rows[1:]
    parts = [
        '<table class="docutils align-default">',
        "<thead><tr><th>{}</th><th>{}</th></tr></thead>".format(
            html_escape(header[0]), html_escape(header[1])
        ),
        "<tbody>",
    ]
    for c1, c2 in body:
        value = c2
        if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
            value = value[1:-1]
            rendered = (
                '<span class="math notranslate nohighlight">\\({}\\)</span>'.format(
                    html_escape(value)
                )
            )
        else:
            rendered = html_escape(value)
        parts.append(
            "<tr><td>{}</td><td>{}</td></tr>".format(html_escape(c1), rendered)
        )
    parts.extend(["</tbody>", "</table>"])
    parts.append(_CHUNK_MATHJAX_BOOTSTRAP)
    return "\n".join(parts) + "\n"


def _discover_lazychunks_folders(src_dir: Path) -> set[str]:
    folders: set[str] = set()
    for rst_file in src_dir.rglob("*.rst"):
        try:
            text = rst_file.read_text(encoding="utf-8")
        except OSError:
            continue
        for options, content in _parse_lazychunks_blocks(text):
            if "csv" in options:
                continue
            for item in content:
                if "|" not in item:
                    folders.add(item)
    return folders


def _discover_csv_specs(src_dir: Path) -> list[tuple[str, Path, int]]:
    specs: dict[tuple[str, str, int], tuple[str, Path, int]] = {}
    for rst_file in src_dir.rglob("*.rst"):
        try:
            text = rst_file.read_text(encoding="utf-8")
        except OSError:
            continue
        for options, content in _parse_lazychunks_blocks(text):
            if "csv" not in options:
                continue
            csv_value = options["csv"]
            csv_path = _resolve_csv_path(src_dir, csv_value)
            max_rows_str = options.get("max-rows", "100").strip() or "100"
            try:
                max_rows = int(max_rows_str)
            except ValueError:
                continue
            if max_rows <= 0:
                continue
            dataset = content[0] if content else Path(csv_value).stem
            key = (dataset, str(csv_path), max_rows)
            specs[key] = (dataset, csv_path, max_rows)
    return [specs[k] for k in sorted(specs)]


def _generate_apn_chunks(app, _exception):
    src_dir = Path(app.srcdir)
    out_chunks = Path(app.outdir) / "_static" / "apn_chunks"
    out_chunks.mkdir(parents=True, exist_ok=True)

    range_re = re.compile(r"^(\d+)_(\d+)$")
    for folder in sorted(_discover_lazychunks_folders(src_dir)):
        includes_base = _resolve_includes_base(src_dir, folder)
        if not includes_base.is_dir():
            continue
        for interval_dir in sorted(includes_base.iterdir()):
            if not interval_dir.is_dir() or not range_re.fullmatch(interval_dir.name):
                continue
            for rst_file in sorted(interval_dir.glob("*.rst")):
                if not range_re.fullmatch(rst_file.stem):
                    continue
                try:
                    html = _list_table_rst_to_html(
                        rst_file.read_text(encoding="utf-8")
                    )
                except OSError:
                    continue
                if not html:
                    continue
                out_file = out_chunks / f"{folder}_{rst_file.stem}.html"
                out_file.write_text(html, encoding="utf-8")

    for dataset, csv_path, max_rows in _discover_csv_specs(src_dir):
        if not csv_path.is_file():
            continue
        try:
            header, rows = _read_csv_table(csv_path)
        except OSError:
            continue
        for stale in out_chunks.glob(f"{dataset}_*.html"):
            try:
                stale.unlink()
            except OSError:
                continue
        for start, end, _first_id, _last_id in _csv_chunk_meta(rows, max_rows):
            html = _csv_rows_to_html(header, rows[start - 1:end])
            if not html:
                continue
            out_file = out_chunks / f"{dataset}_{start}_{end}.html"
            out_file.write_text(html, encoding="utf-8")


def setup(app):
    app.add_directive("lazychunks", LazyChunksDirective)
    app.connect("build-finished", _generate_apn_chunks)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
