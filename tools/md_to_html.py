"""md_to_html.py — převede markdown na stylované HTML (A4, paleta VoltPlán) pro tisk do PDF.

    python tools/md_to_html.py <vstup.md> <vystup.html> [--compact]

--compact = menší font/mezery (pro 1 A4 shrnutí).
"""
import sys
import pathlib
import markdown

ACCENT = "#1F6F5C"
INK = "#23211E"
MUTED = "#6E6A63"
BORDER = "#E6E4DF"

CSS = """
@page {{ size: A4; margin: {pm}; }}
* {{ box-sizing: border-box; }}
body {{
    font-family: -apple-system, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    color: {ink}; font-size: {fs}; line-height: {lh}; margin: 0;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
h1 {{ font-size: {h1}; color: {ink}; letter-spacing: -0.02em; margin: 0 0 .2em;
     border-bottom: 3px solid {accent}; padding-bottom: .25em; }}
h2 {{ font-size: {h2}; color: {accent}; margin: {h2mt} 0 .3em;
     border-bottom: 1px solid {border}; padding-bottom: .12em; }}
h3 {{ font-size: {h3}; color: {ink}; margin: .8em 0 .25em; }}
p, li {{ margin: .25em 0; }}
ul, ol {{ margin: .25em 0 .45em; padding-left: 1.3em; }}
strong {{ color: {ink}; }}
code {{ background: #F2F1ED; border-radius: 4px; padding: 1px 5px; font-size: .92em;
       font-family: "SF Mono", Menlo, monospace; }}
pre {{ background: #F7F6F3; border: 1px solid {border}; border-radius: 8px;
      padding: 10px 12px; overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
table {{ border-collapse: collapse; width: 100%; margin: .5em 0; font-size: .95em; }}
th {{ background: {accent}; color: #fff; text-align: left; padding: 5px 9px; font-weight: 600; }}
td {{ border: 1px solid {border}; padding: 4px 9px; vertical-align: top; }}
tr:nth-child(even) td {{ background: #FAFAF8; }}
blockquote {{ border-left: 3px solid {accent}; margin: .6em 0; padding: .3em .9em;
             background: #F4F8F6; color: {ink}; border-radius: 0 6px 6px 0; }}
hr {{ border: none; border-top: 1px solid {border}; margin: 1em 0; }}
a {{ color: {accent}; text-decoration: none; }}
h2 {{ page-break-after: avoid; }}
table, pre, blockquote {{ page-break-inside: avoid; }}
"""


def main():
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    compact = "--compact" in sys.argv

    sizes = dict(fs="8.6pt", lh="1.24", h1="16pt", h2="10.8pt", h3="9.5pt",
                 pm="10mm 13mm", h2mt=".62em") if compact \
        else dict(fs="10.2pt", lh="1.42", h1="20pt", h2="13pt", h3="11pt",
                  pm="14mm 15mm", h2mt="1.1em")

    html_body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    css = CSS.format(ink=INK, accent=ACCENT, muted=MUTED, border=BORDER, **sizes)
    doc = f"<!doctype html><html lang='cs'><head><meta charset='utf-8'>" \
          f"<style>{css}</style></head><body>{html_body}</body></html>"
    out.write_text(doc, encoding="utf-8")
    print(f"HTML → {out}")


if __name__ == "__main__":
    main()
