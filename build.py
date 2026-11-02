"""Build the static GitHub Pages site from site/ and its publication data."""

import json
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE = ROOT / "site"
OUTPUT = ROOT / "docs"


def render_authors(authors):
    rendered = []
    for author in authors:
        if isinstance(author, str):
            rendered.append(escape(author))
            continue
        name = escape(author["name"])
        marker = escape(author.get("marker", ""))
        rendered.append(name + (f"<sup>{marker}</sup>" if marker == "†" else marker))
    return ", ".join(rendered)


def render_paper(item, index):
    panel_id = f"paper-{index}"
    expanded = False
    fields = []

    def field(label, value, class_name=""):
        if value:
            label_class = ' class="abstract-label"' if class_name == "abstract" else ""
            value_class = f' class="{class_name}"' if class_name else ""
            fields.append(f"                    <dt{label_class}>{label}:</dt>")
            fields.append(f"                    <dd{value_class}>{value}</dd>")

    field("Author", render_authors(item["authors"]) if item.get("authors") else None)
    field("Year", escape(str(item["year"])) if item.get("year") else None)
    field("Publication", escape(item["publication"]) if item.get("publication") else None)
    if item.get("doi"):
        doi = escape(item["doi"])
        field("DOI", f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">{doi}</a>')
    field("Abstract", escape(item["abstract"]) if item.get("abstract") else None, "abstract")

    pdf = item.get("pdf")
    if pdf and not (ROOT / pdf).is_file():
        raise FileNotFoundError(f"Missing paper PDF: {pdf}")
    pdf_link = ""
    if pdf:
        pdf_link = (
            f'                  <a class="pill outline pdf-link" href="{escape(pdf, quote=True)}" '
            'target="_blank" rel="noopener">View PDF</a>'
        )
    closed = "" if expanded else " is-closed"
    inert = "" if expanded else " inert"
    field_markup = "\n".join(fields)
    return f'''          <article class="paper">
            <button class="paper-trigger" type="button" aria-expanded="{str(expanded).lower()}" aria-controls="{panel_id}">
              <span class="toggle" aria-hidden="true"></span>
              <span class="paper-title">{escape(item["title"])}</span>
            </button>
            <div class="paper-panel{closed}" id="{panel_id}"{inert}>
              <div class="paper-panel-inner">
                <div class="paper-body">
                  <dl class="paper-fields">
{field_markup}
                  </dl>
{pdf_link}
                </div>
              </div>
            </div>
          </article>'''


def main():
    papers = json.loads((SOURCE / "research.json").read_text(encoding="utf-8"))
    template = (SOURCE / "template.html").read_text(encoding="utf-8")
    if template.count("{{RESEARCH_ITEMS}}") != 1:
        raise ValueError("Expected one research placeholder in template")
    paper_markup = "\n".join(render_paper(item, i) for i, item in enumerate(papers, 1))
    html = template.replace("          {{RESEARCH_ITEMS}}", paper_markup)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    for name in ("site.css", "site.js"):
        shutil.copyfile(SOURCE / name, OUTPUT / name)


if __name__ == "__main__":
    main()
