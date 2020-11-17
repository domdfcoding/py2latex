#!/usr/bin/env python3
#
#  __init__.py
"""
Create LaTeX documents with Python, Markdown and Jinja2.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Iterable

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
import py2latex.templates

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "MIT License"
__version__ = "0.0.6"
__email__ = "dominic@davis-foster.co.uk"

__all__ = ["make_document"]

main_template = py2latex.templates.templates.get_template("main.tex")


def make_document(
		outfile: PathLike,
		*elements: Iterable[str],
		glossary: str = '',
		):
	r"""
	Construct a LaTeX document from the given elements.

	:param outfile:
	:param \*elements:
	:param glossary:
	"""

	outfile = PathPlus(outfile)
	outfile.write_clean(main_template.render(elements=elements, glossary=glossary))
