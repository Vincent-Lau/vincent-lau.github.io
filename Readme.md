# Academic Website of Vincent Lau

The published GitHub Pages site lives in `docs/`. Its current source is in `site/`.

- Edit `site/template.html` for page content and structure.
- Edit `site/site.css` and `site/site.js` for styling and interactions.
- Add papers to `site/research.json`. Each paper needs a `title`; `authors`, `year`, `publication`, `doi`, `abstract`, and `pdf` are optional and appear only when supplied. An author can be a name string or an object with `name` and `marker` (for example, `†`).
- Run `python build.py` to update `docs/` before committing.

The older Quarto files are retained for reference; they do not generate the current page.
