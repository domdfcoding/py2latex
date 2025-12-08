#!/usr/bin/env python
#
#  __init__.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Parts based on https://github.com/rufuspollock/markdown2latex
#  BSD Licensed
#  Authored by Rufus Pollock: <http://www.rufuspollock.org/>
#  Reworked by Julian Wulfheide (ju.wulfheide@gmail.com) and
#  Pedro Gaudencio (pmgaudencio@gmail.com)
#

# stdlib
import os
import pathlib
import re
from typing import Union

# 3rd party
import markdown
import markdown.treeprocessors
import markdown.util

# this package
from py2latex.markdown_parser.images import ImageTextPostProcessor
from py2latex.markdown_parser.links import LinkTextPostProcessor
from py2latex.markdown_parser.maths import MathTextPostProcessor
from py2latex.markdown_parser.tables import TableTextPostProcessor
from py2latex.markdown_parser.utils import escape_latex_entities, unescape_html_entities

__all__ = [
		"LaTeXExtension",
		"LaTeXTreeProcessor",
		"UnescapeHtmlTextPostProcessor",
		"gls",
		"load_markdown",
		"parse_markdown"
		]


def gls(name):
	return rf"\gls{{{name}}}"


def load_markdown(filename: Union[str, pathlib.Path, os.PathLike]) -> str:

	if not isinstance(filename, pathlib.Path):
		filename = pathlib.Path(filename)

	return parse_markdown(filename.read_text())


def parse_markdown(string):
	out = md.convert(string)

	out = re.sub(r"</?root>", '', out)

	out = re.sub(r"gls{([^}]*)}", r"\\gls{\1}", out)
	out = re.sub(r"citep{([^}]*)}", r"~\\citep{\1}", out)
	out = re.sub(r"cite{([^}]*)}", r"~\\cite{\1}", out)

	# text_md = re.sub(r"\*\*(.+)\*\*", r"\\textbf{\1}", text_md)
	# text_md = re.sub(r"\*(.+)\*", r"\\textit{\1}", text_md)
	out = re.sub(r"<sup>(.+)</sup>", r"\\textsuperscript{\1}", out)
	out = re.sub(r"<sub>(.+)</sub>", r"\\textsubscript{\1}", out)
	out = re.sub(r"<sub>(.+)</sub>", r"\\textsubscript{\1}", out)

	return out


class LaTeXExtension(markdown.extensions.Extension):

	def __init__(self, configs=None):
		self.reset()

	def extendMarkdown(self, md, md_globals):  # type: ignore[override]
		self.md = md

		# remove escape pattern -- \\(.*) -- as this messes up any embedded
		# math and we don't need to escape stuff any more for html
		# for key, pat in self.md.inlinePatterns.items():
		#     if pat.pattern == markdown.inlinepatterns.ESCAPE_RE:
		#         self.md.inlinePatterns.pop(key)
		#         break

		# footnote_extension = FootnoteExtension()
		# footnote_extension.extendMarkdown(md, md_globals)

		latex_tp = LaTeXTreeProcessor()
		math_pp = MathTextPostProcessor()
		table_pp = TableTextPostProcessor()
		image_pp = ImageTextPostProcessor()
		link_pp = LinkTextPostProcessor()
		unescape_html_pp = UnescapeHtmlTextPostProcessor()

		md.treeprocessors["latex"] = latex_tp
		md.postprocessors["unescape_html"] = unescape_html_pp
		md.postprocessors["math"] = math_pp
		md.postprocessors["image"] = image_pp
		md.postprocessors["table"] = table_pp
		md.postprocessors["link"] = link_pp

	def reset(self):
		pass


class LaTeXTreeProcessor(markdown.treeprocessors.Treeprocessor):

	def run(self, doc):
		"""
		Walk the DOM converting relevant nodes to text nodes with relevant content.
		"""

		latex_text = self.tolatex(doc)

		doc.clear()
		latex_node = markdown.util.etree.Element("root")  # type: ignore[attr-defined]
		latex_node.text = latex_text
		doc.append(latex_node)

	def tolatex(self, ournode):
		buffer = ''
		subcontent = ''

		if ournode.text:
			subcontent += escape_latex_entities(ournode.text)

		if ournode.getchildren():
			for child in ournode.getchildren():
				subcontent += self.tolatex(child)

		if ournode.tag == "h1":
			buffer += f"\n\\chapter{{{subcontent}}}"
			buffer += f"'\n\\label{{chapter:{subcontent.lower().replace(' ', '_')}}}\n'"

		elif ournode.tag == "h2":
			buffer += f"\n\n\\section{{{subcontent}}}"
			buffer += f"'\n\\label{{section:{subcontent.lower().replace(' ', '_')}}}\n'"
		elif ournode.tag == "h3":
			buffer += f"\n\n\\subsection{{{subcontent}}}"
			buffer += f"'\n\\label{{subsection:{subcontent.lower().replace(' ', '_')}}}\n'"
		elif ournode.tag == "h4":
			buffer += f"\n\\subsubsection{{{subcontent}}}"
			buffer += f"'\n\\label{{subsubsection:{subcontent.lower().replace(' ', '_')}}}\n'"
		elif ournode.tag == "hr":
			buffer += "\\noindent\\makebox[\\linewidth]{\\rule{\\linewidth}{0.4pt}}"
		elif ournode.tag == "ul":
			# no need for leading \n as one will be provided by li
			buffer += f"""
\\begin{{itemize}}{subcontent}
\\end{{itemize}}
"""
		elif ournode.tag == "ol":
			# no need for leading \n as one will be provided by li
			buffer += f"""
\\begin{{enumerate}}{subcontent}
\\end{{enumerate}}
"""
		elif ournode.tag == "li":
			buffer += f"""
	\\item {subcontent.strip()}"""
		elif ournode.tag == "blockquote":
			# use quotation rather than quote as quotation can support multiple
			# paragraphs
			buffer += f"""
\\begin{{quotation}}
{subcontent.strip()}
\\end{{quotation}}
"""
		# ignore 'code' when inside pre tags
		# (mkdn produces <pre><code></code></pre>)
		elif (
				ournode.tag == "pre"
				or (ournode.tag == "pre" and ournode.parentNode.tag != "pre")  # TODO: Take a look here
				):
			buffer += f"""
\\begin{{verbatim}}
{subcontent.strip()}
\\end{{verbatim}}
"""
		elif ournode.tag == 'q':
			buffer += f"`{subcontent.strip()}'"
		elif ournode.tag == 'p':
			buffer += f"\n{subcontent.strip()}\n"
		# Footnote processor inserts all of the footnote in a sup tag
		elif ournode.tag == "sup":
			buffer += f"\\footnote{{{subcontent.strip()}}}"
		elif ournode.tag == "strong":
			buffer += f"\\textbf{{{subcontent.strip()}}}"
		elif ournode.tag == "em":
			buffer += f"\\emph{{{subcontent.strip()}}}"
		# Keep table strcuture. TableTextPostProcessor will take care.
		elif ournode.tag == "table":
			buffer += f"\n\n<table>{subcontent}</table>\n\n"
		elif ournode.tag == "thead":
			buffer += f"<thead>{subcontent}</thead>"
		elif ournode.tag == "tbody":
			buffer += f"<tbody>{subcontent}</tbody>"
		elif ournode.tag == "tr":
			buffer += f"<tr>{subcontent}</tr>"
		elif ournode.tag == "th":
			buffer += f"<th>{subcontent}</th>"
		elif ournode.tag == "td":
			buffer += f"<td>{subcontent}</td>"
		elif ournode.tag == "img":
			buffer += f'<img src=\"{ournode.get("src")}\" alt=\"{ournode.get("alt")}\" />'
		elif ournode.tag == 'a':
			buffer += f'<a href=\"{ournode.get("href")}\">{subcontent}</a>'
		else:
			buffer = subcontent

		if ournode.tail:
			buffer += escape_latex_entities(ournode.tail)

		return buffer


class UnescapeHtmlTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, text):
		return unescape_html_entities(text)


md = markdown.Markdown()
latex_mdx = LaTeXExtension()
latex_mdx.extendMarkdown(md, markdown.__dict__)
