#  !/usr/bin/env python
#
#  formatting.py
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
from typing import Union


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
