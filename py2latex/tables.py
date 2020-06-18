#  !/usr/bin/env python
#
#  tables.py
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
from textwrap import indent
from typing import Iterable, List, Optional, Sequence, Union

# 3rd party
import tabulate
from tabulate import Line, TableFormat

# this package
from py2latex.core import begin, make_caption, make_label, re_escape
from py2latex.templates import templates

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


def _latex_line_begin_tabular(colwidths, colaligns, booktabs=False, longtable=False, longtable_continued=False):
	"""
	Based on Bart Broere's fork of python-tabulate
	https://github.com/bartbroere/python-tabulate
	MIT Licensed

	https://pypi.org/project/tabulate/
	"""

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

raw_longbooktab_cont = latex_format_builder(raw=True, booktabs=True, longtable=True, longtable_continued=True)


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
	# table = table.replace(
	# 		toprule,
	# 		"".join([*elems, "\\\\\n", toprule, "\n\\endfirsthead\n", f"\\caption*{{{caption}}}\\\\\n"])
	# 		)

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
				fr"{re_escape(begin(environment))}(\[[^\]]*\])?{{.*}}",
				fr"{re_escape(begin(environment))}{{{widths}}}",
				table,
				)

	return table


_longtable_template = templates.get_template("longtable.tex")
_table_template = templates.get_template("table.tex")
_subtables_template = templates.get_template("subtables.tex")
_subtables_template.globals["indent"] = indent  # type: ignore


def longtable_from_template(
		tabular_data,
		*,
		caption: str,
		label: Optional[str] = None,
		headers: Sequence[str] = (),
		pos: str = "htpb",
		floatfmt: str = tabulate._DEFAULT_FLOATFMT,  # type: ignore
		numalign: str = "decimal",
		stralign: str = "left",
		missingval: str = tabulate._DEFAULT_MISSINGVAL,  # type: ignore
		showindex: str = "default",
		disable_numparse: bool = False,
		colalign: Optional[Sequence[Union[str, None]]] = None,
		colwidths: Optional[Sequence[Union[str, None]]] = None,
		vlines: Union[Sequence[int], bool] = False,
		hspace: Union[Sequence[int], bool] = False,
		raw: bool = True,
		footer: Optional[str] = None,
		) -> str:
	"""
	Create a ``longtable`` with ``booktabs`` formatting.

	:param tabular_data:
	:type tabular_data:
	:param caption: The caption for the table
	:type caption: str
	:param label: The label for the table.
		If undefined the caption is used, in lowercase, with underscores replacing spaces
	:param headers: A sequence of column headers
	:param pos: The positioning of the table, e.g. ``"htp"``
	:type pos: str
	:param floatfmt: The formatting of :class:`float` values. Default ``"g"``
	:type floatfmt: str
	:param numalign:
	:type numalign:
	:param stralign:
	:type stralign:
	:param missingval:
	:type missingval:
	:param showindex:
	:type showindex:
	:param disable_numparse:
	:type disable_numparse:
	:param colalign:
	:param colwidths: Sequence of column widths, e.g. ``3cm``. Values of :py:obj:`None` indicates auto width
	:param vlines: If a sequence of integers a line will be inserted before the specified columns. ``-1`` indicates a line should be inserted after the last column.
		If :py:obj:`True` a line will be inserted before every column, and after the last column.
		If :py:obj:`False` no lines will be inserted.
	:param hspace: If a sequence of integers extra space will be inserted before the specified row. ``-1`` indicates a space should be inserted after the last row.
		If :py:obj:`True` a space will be inserted before every row, and after the last row.
		If :py:obj:`False` no spaces will be inserted.
	:param raw: Whether latex markup in ``tabular_data`` should be unescaped. Default ``True``
	:type raw: bool
	:param footer: Optional footer for the table. Inserted as raw LaTeX

	:return:
	:rtype: str
	"""

	return table_from_template(
			tabular_data,
			caption=caption,
			label=label,
			headers=headers,
			pos=pos,
			floatfmt=floatfmt,
			numalign=numalign,
			stralign=stralign,
			missingval=missingval,
			showindex=showindex,
			disable_numparse=disable_numparse,
			colalign=colalign,
			colwidths=colwidths,
			vlines=vlines,
			hspace=hspace,
			raw=raw,
			footer=footer,
			longtable=True,
			)


def _make_body_only_formats(raw=False):

	if raw:
		datarow = headerrow = partial(tabulate._latex_row, escrules={})  # type: ignore
	else:
		datarow = headerrow = tabulate._latex_row  # type: ignore

	return TableFormat(
			lineabove=None,
			linebelowheader=None,
			linebelow=None,
			datarow=datarow,
			headerrow=headerrow,
			linebetweenrows=None,
			padding=1,
			with_header_hide=None,
			)


body_only_format = _make_body_only_formats(raw=False)
raw_body_only_format = _make_body_only_formats(raw=True)


def _parse_rows(
		rows: List[str],
		tabular_data,
		headers: Sequence[str] = (),
		):

	if headers:
		header_row = rows[0]
		body_rows = rows[1:]
		ncols = len(headers)
	else:
		header_row = ''
		body_rows = rows
		ncols = len(tabular_data[0])

	return header_row, body_rows, ncols


def parse_hspace(ncols: int, hspace: Union[Sequence[int], bool] = False):

	if isinstance(hspace, Sequence):
		add_hspace = True
	else:
		add_hspace = bool(hspace)
		hspace = list(range(ncols))

	return add_hspace, hspace


def table_from_template(
		tabular_data,
		*,
		caption: str,
		label: Optional[str] = None,
		headers: Sequence[str] = (),
		pos: str = "htpb",
		floatfmt: str = tabulate._DEFAULT_FLOATFMT,  # type: ignore
		numalign: str = "decimal",
		stralign: str = "left",
		missingval: str = tabulate._DEFAULT_MISSINGVAL,  # type: ignore
		showindex: str = "default",
		disable_numparse: bool = False,
		colalign: Optional[Sequence[Union[str, None]]] = None,
		colwidths: Optional[Sequence[Union[str, None]]] = None,
		vlines: Union[Sequence[int], bool] = False,
		hspace: Union[Sequence[int], bool] = False,
		raw: bool = True,
		footer: Optional[str] = None,
		longtable: bool = False
		) -> str:
	"""
	Create a ``table`` with ``booktabs`` formatting.

	:param tabular_data:
	:type tabular_data:
	:param caption: The caption for the table
	:type caption: str
	:param label: The label for the table.
		If undefined the caption is used, in lowercase, with underscores replacing spaces
	:param headers: A sequence of column headers
	:param pos: The positioning of the table, e.g. ``"htp"``
	:type pos: str
	:param floatfmt: The formatting of :class:`float` values. Default ``"g"``
	:type floatfmt: str
	:param numalign:
	:type numalign:
	:param stralign:
	:type stralign:
	:param missingval:
	:type missingval:
	:param showindex:
	:type showindex:
	:param disable_numparse:
	:type disable_numparse:
	:param colalign:
	:param colwidths: Sequence of column widths, e.g. ``3cm``. Values of :py:obj:`None` indicates auto width
	:param vlines: If a sequence of integers a line will be inserted before the specified columns. ``-1`` indicates a line should be inserted after the last column.
		If :py:obj:`True` a line will be inserted before every column, and after the last column.
		If :py:obj:`False` no lines will be inserted.
	:param hspace: If a sequence of integers extra space will be inserted before the specified row. ``-1`` indicates a space should be inserted after the last row.
		If :py:obj:`True` a space will be inserted before every row, and after the last row.
		If :py:obj:`False` no spaces will be inserted.
	:param raw: Whether latex markup in ``tabular_data`` should be unescaped. Default ``False``
	:type raw: bool
	:param footer: Optional footer for the table. Inserted as raw LaTeX
	:param longtable: Whether to create a ``longtable``. Default :py:obj:`False``
	:type longtable: bool

	:return:
	:rtype: str
	"""

	table = SubTable(
			tabular_data,
			caption=caption,
			label=label,
			headers=headers,
			floatfmt=floatfmt,
			numalign=numalign,
			stralign=stralign,
			missingval=missingval,
			showindex=showindex,
			disable_numparse=disable_numparse,
			colalign=colalign,
			colwidths=colwidths,
			vlines=vlines,
			hspace=hspace,
			raw=raw,
			footer=footer,
			)

	if longtable:
		return _longtable_template.render(
				caption=table.caption,
				label=table.label,
				header_row=table.header_row,
				table_body=table.table_body,
				ncols=table.ncols,
				colalign=table.colalign,
				pos=pos,
				footer=table.footer,
				)

	else:
		return _table_template.render(
				caption=table.caption,
				label=table.label,
				header_row=table.header_row,
				table_body=table.table_body,
				ncols=table.ncols,
				colalign=table.colalign,
				pos=pos,
				footer=table.footer,
				)


class SubTable:

	def __init__(
			self,
			tabular_data,
			*,
			caption: str,
			label: Optional[str] = None,
			headers: Sequence[str] = (),
			floatfmt: str = tabulate._DEFAULT_FLOATFMT,  # type: ignore
			numalign: str = "decimal",
			stralign: str = "left",
			missingval: str = tabulate._DEFAULT_MISSINGVAL,  # type: ignore
			showindex: str = "default",
			disable_numparse: bool = False,
			colalign: Optional[Sequence[Union[str, None]]] = None,
			colwidths: Optional[Sequence[Union[str, None]]] = None,
			vlines: Union[Sequence[int], bool] = False,
			hspace: Union[Sequence[int], bool] = False,
			raw: bool = True,
			footer: Optional[str] = None,
			) -> None:

		if raw:
			tablefmt = raw_body_only_format
		else:
			tablefmt = body_only_format

		rows = tabulate.tabulate(
				tabular_data,
				tablefmt=tablefmt,
				headers=headers,
				floatfmt=floatfmt,
				numalign=numalign,
				stralign=stralign,
				missingval=missingval,
				showindex=showindex,
				disable_numparse=disable_numparse,  # colalign=colalign,
				).split("\n")

		header_row, body_rows, ncols = _parse_rows(rows, tabular_data, headers)
		add_hspace, hspace = parse_hspace(ncols, hspace)
		col_alignment = parse_column_alignments(colalign, colwidths, vlines, ncols)

		table_body = ''
		for row_idx, row in enumerate(body_rows):
			row = re.sub(r"(\\multicolumn{2\}{.*\}{{.*\}\}\s*)&", r"\1 ", row)
			row = re.sub(r"(\\multicolumn{3\}{.*\}{{.*\}\}\s*)&(\s*)&", r"\1 \2", row)
			row = re.sub(r"(\\multicolumn{4\}{.*\}{{.*\}\}\s*)&(\s*)&(\s*)&", r"\1 \2 \3", row)
			row = re.sub(r"(\\multicolumn{5\}{.*\}{{.*\}\}\s*)&(\s*)&(\s*)&(\s*)&", r"\1 \2 \3 \4", row)

			if add_hspace and row_idx in hspace:  # type: ignore
				table_body += "\\addlinespace"

			table_body += f"{row}\n"

		if not label:
			label = caption.lower().replace(" ", "_")

		self.caption: str = str(caption)
		self.label: str = str(label)
		self.header_row: str = header_row
		self.table_body: str = indent(table_body, "       ")
		self.ncols: int = ncols
		self.colalign: str = "".join(col_alignment)
		self.footer: str = str(footer)


def subtables_from_template(
		subtables: Iterable[SubTable],
		*,
		caption: str,
		label: Optional[str] = None,
		pos: str = "htpb",
		) -> str:
	# TODO: customise spacing between tables
	"""
	Create a series of ``subtables`` with ``booktabs`` formatting.

	:param subtables:
	:type subtables:
	:param caption: The caption for the table
	:type caption: str
	:param label: The label for the table.
		If undefined the caption is used, in lowercase, with underscores replacing spaces
	:param pos: The positioning of the table, e.g. ``"htp"``
	:type pos: str

	:return:
	:rtype: str
	"""

	if not label:
		label = caption.lower().replace(" ", "_")

	return _subtables_template.render(
			subtables=subtables,
			caption=caption,
			label=label,
			pos=pos,
			)


def parse_column_alignments(colalign, colwidths, vlines, ncols):
	if colalign is None:
		colalign = ["l"] * ncols

	while len(colalign) < ncols:
		colalign.append("l")

	alignment_elements = []

	if colwidths is None:
		colwidths = [None] * ncols

	while len(colwidths) < ncols:
		colwidths.append(None)

	if isinstance(vlines, Sequence):
		add_vlines = True
	else:
		add_vlines = bool(vlines)
		vlines = list(range(ncols + 1))

	col_idx = 0

	for col_idx, (alignment, width) in enumerate(zip(colalign, colwidths)):
		# print(col_idx, alignment, width)

		if add_vlines and col_idx in vlines:
			alignment_elements.append("|")

		if alignment.startswith("l"):
			if width is None:
				alignment_elements.append("l")
			else:
				alignment_elements.append(fr">{{\raggedright}}p{{{width}}}")

		elif alignment.startswith("r") or alignment.lower() == "decimal":
			if width is None:
				alignment_elements.append("r")
			else:
				alignment_elements.append(fr">{{\raggedleft\arraybackslash}}p{{{width}}}")

		# TODO: centered and width

		elif alignment.startswith("c"):
			alignment_elements.append("c")

		elif alignment.startswith("p"):
			if width is None:
				raise ValueError(f"Must specify width for 'p' column with index {col_idx}")
			else:
				alignment_elements.append(fr">{{\raggedleft\arraybackslash}}p{{{width}}}")

	if add_vlines:
		if col_idx + 1 in vlines or -1 in vlines:
			alignment_elements.append("|")

	return "".join(alignment_elements)


templates.globals["brace"] = lambda var: f"{{{var}}}"

if __name__ == '__main__':

	# stdlib
	from pprint import pprint

	pprint(
			longtable_from_template([
					[1, 2, 3, 4, 5],
					[1, 2, 3, 4, 5],
					[1, 2, 3, 4, 5],
					[1, 2, 3, 4, 5],
					],
									headers=["Foo", "Bar", "Baz", "Fizz", "Buzz"],
									caption="My Caption")
			)
