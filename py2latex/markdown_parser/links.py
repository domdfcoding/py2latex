#!/usr/bin/env python
#
#  links.py
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
import re
import xml.dom.minidom
from typing import List

# 3rd party
import markdown.postprocessors

__all__ = ["link_to_Latex", "LinkTextPostProcessor"]


class LinkTextPostProcessor(markdown.postprocessors.Postprocessor):
	"""
	Markdown postprocessor to convert hyperlinks to LaTeX.
	"""

	def run(self, text) -> str:
		"""
		Transforms the given HTML document (as a string) to convert hyperlinks to LaTeX.

		:param text:
		"""

		# Process all hyperlinks

		new_blocks: List[str] = []

		for block in text.split("\n\n"):
			stripped = block.strip()
			match = re.search(r"<a[^>]*>([^<]+)</a>", stripped)
			# <table catches modified versions (e.g. <table class="..">

			if match:
				latex_link = re.sub(r"<a[^>]*>([^<]+)</a>", link_to_Latex(match.group(0)).strip(), stripped)
				new_blocks.append(latex_link)
			else:
				new_blocks.append(block)

		return "\n\n".join(new_blocks)


def link_to_Latex(link_str: str) -> str:
	"""
	Convert an HTML link to its latex equivalent.
	"""

	dom = xml.dom.minidom.parseString(link_str)
	link = dom.documentElement
	href = link.getAttribute("href")

	desc = re.search(r">([^<]+)", link_str)
	if desc:
		return f"\n\\href{{{href}}}{{{desc.group(0)[1:]}}}\n"
	else:
		return ''
