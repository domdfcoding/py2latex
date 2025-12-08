#!/usr/bin/env python
#
#  images.py
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
import markdown.postprocessors

__all__ = ["ImageTextPostProcessor", "img_to_latex"]


class ImageTextPostProcessor(markdown.postprocessors.Postprocessor):

	def run(self, instr: str) -> str:
		"""
		Process all img tags.

		Similar to ``process_tables`` this is not very sophisticated.
		For it to work it is expected that ``img`` tags are put in a section of their own
		(that is separated by at least one blank line above and below).
		"""

		new_blocks: List[str] = []

		for block in instr.split("\n\n"):
			stripped = block.strip()
			# <table catches modified verions (e.g. <table class="..">
			if stripped.startswith("<img"):
				latex_img = img_to_latex(stripped).strip()
				new_blocks.append(latex_img)
			else:
				new_blocks.append(block)

		return "\n\n".join(new_blocks)


def img_to_latex(instr: str) -> str:
	dom = xml.dom.minidom.parseString(instr)
	img = dom.documentElement
	assert img is not None
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
