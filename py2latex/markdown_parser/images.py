#!/usr/bin/env python
#
#  images.py
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
import http.client
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.dom.minidom
from typing import List
from urllib.parse import urlparse

# 3rd party
import markdown  # type: ignore

__all__ = ["ImageTextPostProcessor", "Img2Latex"]


class ImageTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, instr) -> str:
		"""Process all img tags

		Similar to process_tables this is not very sophisticated and for it
		to work it is expected that img tags are put in a section of their own
		(that is separated by at least one blank line above and below).
		"""
		converter = Img2Latex()
		new_blocks: List[str] = []
		for block in instr.split("\n\n"):
			stripped = block.strip()
			# <table catches modified verions (e.g. <table class="..">
			if stripped.startswith("<img"):
				latex_img = converter.convert(stripped).strip()
				new_blocks.append(latex_img)
			else:
				new_blocks.append(block)
		return "\n\n".join(new_blocks)


class Img2Latex:

	def convert(self, instr) -> str:
		dom = xml.dom.minidom.parseString(instr)
		img = dom.documentElement
		src = img.getAttribute("src")

		if urlparse(src).scheme != '':
			src_urlparse = urlparse(src)
			conn = http.client.HTTPConnection(src_urlparse.netloc)
			conn.request("HEAD", src_urlparse.path)
			response = conn.getresponse()
			conn.close()

			if response.status == 200:
				filename = os.path.join(tempfile.mkdtemp(), src.split('/')[-1])
				urllib.request.urlretrieve(src, filename)
				src = filename

		alt = img.getAttribute("alt")

		# Using graphicx and ajustbox package for *max width*

		return f"""
			\\begin{{figure}}[H]
			\\centering
			\\includegraphics[max width=\\linewidth]{{{src}}}
			\\caption{{{alt}}}
			\\end{{figure}}
			"""
