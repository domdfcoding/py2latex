# stdlib
import pathlib
import re

# 3rd party
import markdown
import mdx_latex

text_md = pathlib.Path("text.md").read_text()

text_md = re.sub(r"\*\*(.+)\*\*", r"\\textbf{\1}", text_md)
print(re.sub(r"\*(.+)\*", r"\\textit{\1}", text_md))

md = markdown.Markdown()
latex_mdx = mdx_latex.LaTeXExtension()
latex_mdx.extendMarkdown(md, markdown.__dict__)
out = md.convert(pathlib.Path("text.md").read_text())
print(out)
