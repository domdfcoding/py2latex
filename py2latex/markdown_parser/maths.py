#!/usr/bin/env python
#
#  maths.py
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

# 3rd party
import markdown  # type: ignore

# this package
from py2latex.markdown_parser.utils import unescape_latex_entities

__all__ = ["MathTextPostProcessor"]


class MathTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, instr):
		"""Convert all math sections in {text} whether latex, asciimathml or
		latexmathml formatted to latex.

		This assumes you are using $ for inline math and $$ for blocks as your
		mathematics delimiter (*not* the standard asciimathml or latexmathml
		delimiter).
		"""

		def repl_1(matchobj) -> str:
			"""

			:param matchobj:
			:type matchobj:

			:return:
			:rtype: str
			"""

			text = unescape_latex_entities(matchobj.group(1))
			return f"\\[{text}\\]"

		def repl_2(matchobj) -> str:
			"""

			:param matchobj:
			:type matchobj:

			:return:
			:rtype: str
			"""

			text = unescape_latex_entities(matchobj.group(1))
			return f"\\({text}\\)"

		# This $$x=3$$ is block math
		pat = re.compile(r"\$\$([^$]*)\$\$")
		out = pat.sub(repl_1, instr)

		# This $x=3$ is inline math
		pat2 = re.compile(r"\$([^$]*)\$")
		out = pat2.sub(repl_2, out)

		# some extras due to asciimathml
		out = out.replace("\\lt", '<')
		out = out.replace(" * ", " \\cdot ")
		out = out.replace("\\del", "\\partial")

		return out
