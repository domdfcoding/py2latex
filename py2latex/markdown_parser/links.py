#!/usr/bin/env python
#
#  links.py
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
import xml.dom.minidom
from typing import List

# 3rd party
import markdown  # type: ignore

__all__ = ["Link2Latex", "LinkTextPostProcessor"]


class LinkTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, instr) -> str:
		# Process all hyperlinks

		converter = Link2Latex()
		new_blocks: List[str] = []

		for block in instr.split("\n\n"):
			stripped = block.strip()
			match = re.search(r"<a[^>]*>([^<]+)</a>", stripped)
			# <table catches modified versions (e.g. <table class="..">

			if match:
				latex_link = re.sub(r"<a[^>]*>([^<]+)</a>", converter.convert(match.group(0)).strip(), stripped)
				new_blocks.append(latex_link)
			else:
				new_blocks.append(block)

		return "\n\n".join(new_blocks)


class Link2Latex:

	def convert(self, instr) -> str:
		dom = xml.dom.minidom.parseString(instr)
		link = dom.documentElement
		href = link.getAttribute("href")

		desc = re.search(r">([^<]+)", instr)
		if desc:
			return f"""
				\\href{{{href}}}{{{desc.group(0)[1:]}}}
				"""
		else:
			return ''
