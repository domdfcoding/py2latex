#!/usr/bin/env python
#
#  maths.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
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
