#!/usr/bin/env python
#
#  utils.py
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
