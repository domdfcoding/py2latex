#  !/usr/bin/env python
#
#  markdown.py
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
# stdlib
import os
import pathlib
import re
from typing import Union

# 3rd party
import markdown

# this package
import py2latex.mdx_latex

# this package
from .sectioning import make_chapter

md = markdown.Markdown()
latex_mdx = py2latex.mdx_latex.LaTeXExtension()
latex_mdx.extendMarkdown(md, markdown.__dict__)


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


def re_escape(string: str) -> str:
	"""
	Escape literal backslashes for use with re.

	:param string:
	:type string:

	:return:
	:rtype:
	"""

	return string.replace("\\", "\\\\")
