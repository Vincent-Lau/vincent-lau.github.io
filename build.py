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


def render_research(groups):
    sections = []
    paper_index = 1

    for group in groups:
        items = group.get("items", [])
        if not items:
            continue  # 不显示空类别

        papers = []
        for item in items:
            papers.append(render_paper(item, paper_index))
            paper_index += 1  # 跨类别连续编号，避免 HTML ID 重复

        group_id = escape(group["id"], quote=True)
        title = escape(group["title"])
        paper_markup = "\n".join(papers)

        sections.append(
            f'          <div class="research-group" id="{group_id}">\n'
            f'            <h3>{title}</h3>\n'
            f'{paper_markup}\n'
            f'          </div>'
        )

    return "\n".join(sections)


def main():
    groups = json.loads(
        (SOURCE / "research.json").read_text(encoding="utf-8")
    )
    template = (SOURCE / "template.html").read_text(encoding="utf-8")

    placeholder = "{{RESEARCH_GROUPS}}"
    if template.count(placeholder) != 1:
        raise ValueError("Expected one research placeholder in template")

    research_markup = render_research(groups)
    html = template.replace(placeholder, research_markup)

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")

    shutil.copytree(ROOT / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    for name in ("site.css", "site.js"):
        shutil.copyfile(SOURCE / name, OUTPUT / name)


if __name__ == "__main__":
    main()
