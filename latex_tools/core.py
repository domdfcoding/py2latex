#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  core.py
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
import re
from functools import partial
from typing import Optional

# 3rd party
import tabulate
from tabulate import Line, TableFormat


def make_caption(caption):
	r"""
	Akin to \caption{}

	:param caption:
	:type caption:

	:return:
	:rtype:
	"""

	return rf"\caption{{{caption}}}"


def make_label(label):
	r"""
	Akin to \label{}

	:param label:
	:type label:

	:return:
	:rtype:
	"""

	return rf"\label{{{label}}}"


def begin(environment: str, options: Optional[str] = None):
	r"""
	Akin to \begin{environment}

	:param environment:
	:type environment:
	:param options:
	:type options:

	:return:
	:rtype:
	"""

	if options:
		return rf"\begin{{{environment}}}{{{options}}}"
	else:
		return rf"\begin{{{environment}}}"


def end(environment):
	r"""
	Akin to \end{environment}

	:param environment:
	:type environment:

	:return:
	:rtype:
	"""

	return rf"\end{{{environment}}}"


def re_escape(string):
	"""
	Escape literal backslashes for use with re.

	:param string:
	:type string:

	:return:
	:rtype:
	"""

	return string.replace("\\", "\\\\")
