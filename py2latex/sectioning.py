#!/usr/bin/env python
#
#  templates.py
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

# this package
from .templates import templates

__all__ = [
		"make_chapter",
		"make_paragraph",
		"make_part",
		"make_section",
		"make_subparagraph",
		"make_subsection",
		"make_subsubsection"
		]

sectioning_template = templates.get_template("sectioning.tex")

# 			body=pathlib.Path(filename).read_text(),


def _make_section(section_type, title, body='', label=None, shorttitle=None, unnumbered=False):

	if not label:
		label = f"{section_type}:{title.lower().replace(' ', '_')}"

	return sectioning_template.render(
			section_type=section_type,
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_part(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"part",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_chapter(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"chapter",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_section(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"section",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_subsection(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"subsection",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_subsubsection(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"subsubsection",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_paragraph(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"paragraph",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)


def make_subparagraph(title, body='', label=None, shorttitle=None, unnumbered=False):
	return _make_section(
			"subparagraph",
			title=title,
			label=label,
			body=body,
			shorttitle=shorttitle,
			unnumbered=unnumbered,
			)
