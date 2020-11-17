#!/usr/bin/env python
#
#  templates.py
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

# this package
from py2latex.templates import templates

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
