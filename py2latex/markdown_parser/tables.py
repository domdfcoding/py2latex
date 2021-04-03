#!/usr/bin/env python
#
#  tables.py
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
import xml.dom.minidom
from typing import List

# 3rd party
import markdown.postprocessors  # type: ignore

# this package
from py2latex.markdown_parser.utils import escape_latex_entities

__all__ = ["Table2Latex", "TableTextPostProcessor"]


class TableTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, instr):
		"""
		This is not very sophisticated and for it to work it is expected that:

			1. tables to be in a section on their own (that is at least one
			blank line above and below)
			2. no nesting of tables
		"""

		converter = Table2Latex()
		new_blocks: List[str] = []

		for block in instr.split("\n\n"):
			stripped = block.strip()
			# <table catches modified verions (e.g. <table class="..">
			if stripped.startswith("<table") and stripped.endswith("</table>"):
				latex_table = converter.convert(stripped).strip()
				new_blocks.append(latex_table)
			else:
				new_blocks.append(block)
		return "\n\n".join(new_blocks)


class Table2Latex:
	"""
	Convert html tables to Latex.

	.. TODO:: escape latex entities.
	"""

	numcols: int
	maxcols: int

	def colformat(self):
		# centre align everything by default
		out = "|l" * self.maxcols + '|'
		return out

	def get_text(self, element):
		if element.nodeType == element.TEXT_NODE:
			return escape_latex_entities(element.data)
		result = ''
		if element.childNodes:
			for child in element.childNodes:
				text = self.get_text(child)
				if text.strip() != '':
					result += text
		return result

	def process_cell(self, element):
		# works on both td and th
		colspan = 1
		subcontent = self.get_text(element)
		buffer = ''

		if element.tagName == "th":
			subcontent = f"\\textbf{{{subcontent}}}"
		if element.hasAttribute("colspan"):
			colspan = int(element.getAttribute("colspan"))
			buffer += fr" \multicolumn{{{colspan}}}{{|c|}}{{{subcontent}}}"
		# we don't support rowspan because:
		#   1. it needs an extra latex package \usepackage{multirow}
		#   2. it requires us to mess around with the alignment tags in
		#   subsequent rows (i.e. suppose the first col in row A is rowspan 2
		#   then in row B in the latex we will need a leading &)
		# if element.hasAttribute("rowspan"):
		#     rowspan = int(element.getAttribute("rowspan"))
		#     buffer += " \multirow{%s}{|c|}{%s}" % (rowspan, subcontent)
		else:
			buffer += f" {subcontent}"

		notLast = (
				element.nextSibling.nextSibling
				and element.nextSibling.nextSibling.nodeType == element.ELEMENT_NODE
				and element.nextSibling.nextSibling.tagName in ["td", "th"]
				)

		if notLast:
			buffer += " &"

		self.numcols += colspan
		return buffer

	def tolatex(self, element):
		if element.nodeType == element.TEXT_NODE:
			return ''

		buffer = ''
		subcontent = ''
		if element.childNodes:
			for child in element.childNodes:
				text = self.tolatex(child)
				if text.strip() != '':
					subcontent += text
		subcontent = subcontent.strip()

		if element.tagName == "thead":
			buffer += subcontent

		elif element.tagName == "tr":
			self.maxcols = max(self.numcols, self.maxcols)
			self.numcols = 0
			buffer += f"\n\\hline\n{subcontent} \\\\"

		elif element.tagName == "td" or element.tagName == "th":
			buffer = self.process_cell(element)
		else:
			buffer += subcontent
		return buffer

	def convert(self, instr):
		self.numcols = 0
		self.maxcols = 0
		dom = xml.dom.minidom.parseString(instr)
		core = self.tolatex(dom.documentElement)

		captionElements = dom.documentElement.getElementsByTagName("caption")
		caption = ''
		if captionElements:
			caption = self.get_text(captionElements[0])

		colformatting = self.colformat()
		table_latex = f"""
			\\begin{{table}}[h]
			\\begin{{tabular}}{{{colformatting}}}
			{core}
			\\hline
			\\end{{tabular}}
			\\\\[5pt]
			\\caption{{{caption}}}
			\\end{{table}}
			"""
		return table_latex
