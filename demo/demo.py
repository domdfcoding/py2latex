# stdlib
import pathlib
import re

# 3rd party
import jinja2
from jinja2 import Environment, FileSystemLoader

# this package
import py2latex
from py2latex.markdown_parser import load_markdown
from py2latex.sectioning import make_chapter
from py2latex.glossaries import glossary_from_file
# stdlib
from pprint import pprint

chapters_list = []

for title, filename in [
		(f"Chapter 0", "Chapter0.tex"),
		(f"Chapter 1", "Chapter1.tex"),
		(f"Chapter 2", "Chapter2.tex"),
		]:

	body = pathlib.Path(filename).read_text()
	chapters_list.append(make_chapter(title, body=body))

text_md = load_markdown("text.md")

chapters_list.append(make_chapter(title=f"Markdown Chapter", body=text_md))

chapters_list.append(make_chapter(title=f"Introduction", body=load_markdown("introduction.md")))

import astropy.units as u
from py2latex.siunit import si, SI
kgms = u.kg * u.m / u.A / u.s
chapters_list.append(si(kgms))
l3vt3 = u.lux ** 3 * u.V / u.T ** 3
chapters_list.append(si(l3vt3))
chapters_list.append(SI(3*l3vt3))

glossary = glossary_from_file(pathlib.Path("glossary.yaml"))


pprint(glossary)

chapters_list.append(r"\bigskip\huge{\texttt{py}$2$\LaTeX}")

py2latex.make_document("demo.tex", chapters_list, glossary=glossary)
