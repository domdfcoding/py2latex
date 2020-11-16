#!/usr/bin/env python
#
#  utils.py
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

__all__ = ["escape_latex_entities", "re_escape", "unescape_html_entities", "unescape_latex_entities"]


def re_escape(string: str) -> str:
	"""
	Escape literal backslashes for use with re.

	:param string:
	:type string:

	:return:
	:rtype:
	"""

	return string.replace('\\', "\\\\")


start_single_quote_re = re.compile("(^|\\s|\")'")
start_double_quote_re = re.compile("(^|\\s|'|`)\"")
end_double_quote_re = re.compile('"(,|\\.|\\s|$)')


def unescape_html_entities(text: str) -> str:
	"""

	:param text:
	:type text: str

	:return:
	:rtype: str
	"""

	out = text.replace("&amp;", '&')
	out = out.replace("&lt;", '<')
	out = out.replace("&gt;", '>')
	out = out.replace("&quot;", '"')
	return out


def escape_latex_entities(text: str) -> str:
	"""
	Escape latex reserved characters.

	:param text:
	:type text: str

	:return:
	:rtype: str
	"""

	out = text
	out = unescape_html_entities(out)

	out = re.sub(r"[^\n\\]%", r"\\%", out)
	out = re.sub(r"[^\\]&", r"\\&", out)
	out = re.sub(r"[^\\]#", r"\\#", out)

	out = re.sub(r"\"([^\"]*)\"", r"\\enquote{\1}", out)
	out = re.sub(r"\'([^\']*)\'", r"\\enquote{\1}", out)

	# out = start_single_quote_re.sub(r'\g<1>`', out)
	# out = start_double_quote_re.sub(r'\g<1>``', out)
	# out = end_double_quote_re.sub(r"''\g<1>", out)

	# people should escape these themselves as it conflicts with maths
	# out = out.replace('{', '\\{')
	# out = out.replace('}', '\\}')
	# do not do '$' here because it is dealt with by convert_maths
	# out = out.replace('$', '\\$')
	return out


def unescape_latex_entities(text: str) -> str:
	"""
	Limit ourselves as this is only used for maths stuff.

	:param text:
	:type text: str

	:return:
	:rtype: str
	"""

	out = text
	out = out.replace("\\&", '&')
	return out
