#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  tabulate.py
"""
Extension to python-tabulate

https://pypi.org/project/tabulate/
"""
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

# this package
from latex_tools.core import begin, make_caption, make_label, re_escape

hline = r"\hline"
toprule = r"\toprule"
midrule = r"\midrule"
endfoot = r"\endfoot"
endhead = r"\endhead"
bottomrule = r"\bottomrule"
endlastfoot = r"\endlastfoot"
table_linebreak = r"\\"


def multicolumn(cols: int, pos: str, text: str) -> str:
	"""

	:param cols: The number of columms to span
	:type cols: int
	:param pos: Text alignment:
		* c for centered
		* l for flushleft
		* r for flushright
	:type pos: str
	:param text:
	:type text: str

	:return:
	:rtype: str
	"""

	return fr"\multicolumn{{{cols}}}{{{pos}}}{{{{{text}}}}}"


# From https://github.com/bartbroere/python-tabulate
def _latex_line_begin_tabular(colwidths, colaligns, booktabs=False, longtable=False, longtable_continued=False):
	alignment = {"left": "l", "right": "r", "center": "c", "decimal": "r"}
	tabular_columns_fmt = "".join([alignment.get(a, "l") for a in colaligns])

	if longtable:

		line_begin_elements = [rf"\begin{{longtable}}{{{tabular_columns_fmt}}}"]

		if longtable_continued:
			line_begin_elements.append(
					fr"""\midrule
\multicolumn{{{len(colwidths)}}}{{r}}{{{{\small Continued on next page\normalsize}}}} \\
\midrule
\endfoot

\bottomrule
\endlastfoot
"""
					)
	else:
		line_begin_elements = [rf"\begin{{tabular}}{{{tabular_columns_fmt}}}"]

	if booktabs:
		line_begin_elements.append(toprule)
	else:
		line_begin_elements.append(hline)

	return "\n".join(line_begin_elements)


def latex_format_builder(
		raw: bool = False,
		booktabs: bool = False,
		longtable: bool = False,
		longtable_continued: bool = False,
		) -> TableFormat:
	lineabove = partial(
			_latex_line_begin_tabular,
			longtable=longtable,
			booktabs=booktabs,
			longtable_continued=longtable_continued
			)

	if booktabs and longtable:
		linebelowheader = [midrule, endhead]

		if longtable_continued:
			linebelow = [r"\end{longtable}"]
		else:
			linebelow = [bottomrule, r"\end{longtable}"]

	elif booktabs:
		linebelowheader = [midrule]
		linebelow = [bottomrule, r"\end{tabular}"]

	elif longtable:
		linebelowheader = [hline, endhead]
		linebelow = [hline, r"\end{longtable}"]

	else:
		linebelowheader = [hline]
		linebelow = [hline, r"\end{tabular}"]

	if raw:
		datarow = headerrow = partial(tabulate._latex_row, escrules={})  # type: ignore
	else:
		datarow = headerrow = tabulate._latex_row  # type: ignore

	return TableFormat(
			lineabove=lineabove,
			linebelowheader=Line("\n".join(linebelowheader), "", "", ""),
			linebelow=Line("\n".join(linebelow), "", "", ""),
			datarow=datarow,
			headerrow=headerrow,
			linebetweenrows=None,
			padding=1,
			with_header_hide=None,
			)


table_formats = {
		"latex": latex_format_builder(),
		"latex_raw": latex_format_builder(raw=True),
		"latex_booktabs": latex_format_builder(booktabs=True),
		"latex_booktabs_raw": latex_format_builder(raw=True, booktabs=True),
		"latex_longtable": latex_format_builder(longtable=True),
		"latex_longtable_raw": latex_format_builder(raw=True, longtable=True),
		"latex_longtable_booktabs": latex_format_builder(longtable=True, booktabs=True),
		"latex_longtable_booktabs_raw": latex_format_builder(raw=True, longtable=True, booktabs=True),
		}


def add_longtable_caption(table: str, caption: Optional[str] = None, label: Optional[str] = None) -> str:
	"""
	Add a caption to a longtable

	:param table:
	:type table: str
	:param caption: str
	:type caption:
	:param label:
	:type label: str

	:return:
	:rtype:
	"""

	elems = []

	if caption:
		elems.append(make_caption(caption))

	if label:
		elems.append(make_label(label))

	if caption or label:
		table = table.replace(toprule, "".join([*elems, "\\\\\n", toprule]))

	return table


def set_table_widths(table: str, widths: str) -> str:
	"""
	Override the column widths (and also the column alignments) in a tabular environment, etc.

	:param table:
	:type table: str
	:param widths:
	:type widths: str

	:return:
	:rtype: str
	"""

	for environment in {"tabular", "longtable"}:
		table = re.sub(
				fr"{re_escape(begin(environment))}{{.*}}",
				fr"{re_escape(begin(environment))}{{{widths}}}",
				table,
				)

	return table
