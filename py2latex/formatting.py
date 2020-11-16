#!/usr/bin/env python
#
#  formatting.py
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

# stdlib
from typing import Union

__all__ = ["bold", "italic", "latex_subscript", "latex_superscript", "underline"]


def bold(val: Union[str, float]) -> str:
	r"""Make the given value bold

	Akin to \textbf{string}

	:param val: The value to make bold

	:return: The formatted string.
	"""

	return fr"\textbf{{{val}}}"


def underline(val: Union[str, float]) -> str:
	r"""Underline the given value

	Akin to \underline{string}

	:param val: The value to underline

	:return: The formatted string.
	"""

	return fr"\underline{{{val}}}"


def italic(val: Union[str, float]) -> str:
	r"""Make the given value italic

	Akin to \textit{string}

	:param val: The value to make italic

	:return: The formatted string.
	"""

	return fr"\textit{{{val}}}"


def latex_subscript(val: Union[str, float]) -> str:
	"""
	Returns the LaTeX subscript of the given value.

	:param val: The value to superscript

	:rtype: str
	"""

	return f"$_{{{val}}}$"


def latex_superscript(val: Union[str, float]) -> str:
	"""
	Returns the LaTeX superscript of the given value.

	:param val: The value to subscript

	:rtype: str
	"""

	return f"$^{{{val}}}$"
