"""Render the S5–S8 Markdown deliverables with the S4 visual style."""
from pathlib import Path

import markdown

# Reuse the existing S4 rendering setup and styles without rebuilding S4.
SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1]
style_source = (SOURCE / "build_assignment4.py").read_text().split("content = ", 1)[0]
namespace = {"__file__": str(SOURCE / "build_assignment4.py")}
exec(compile(style_source, "build_assignment4.py", "exec"), namespace)
render = namespace["HTML"]
style = namespace["css"]

for number, source, output in (
    ("5", "05_metrics.md", "Assignment_5_Metrics.pdf"),
    ("6–7", "06_07_experiments_operations.md", "Assignment_6_7_Experiments_and_Operations.pdf"),
    ("8", "08_launch_memo.md", "Assignment_8_Launch_Memo.pdf"),
):
    content = (ROOT / source).read_text()
    pages = [content]
    if number == "6–7":
        design, operations = content.split("## 3. Monitoring", 1)
        pages = [design, "## 3. Monitoring" + operations]
    body = "".join(
        "<section>" + markdown.markdown(page, extensions=["tables"]) + "</section>"
        for page in pages
    )
    css = style.replace("ASSIGNMENT 4 · 9 NOVEMBER 2026", f"ASSIGNMENT {number}")
    document = render(
        string=f'<!doctype html><html lang="en"><meta charset="utf-8"><style>{css}</style>{body}</html>',
        base_url=str(ROOT),
    ).render()
    assert len(document.pages) == len(pages), (output, len(document.pages))
    document.write_pdf(ROOT / "assignments" / output)
    print(f"{output}: {len(document.pages)} page(s)")
