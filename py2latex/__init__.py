#!/usr/bin/env python3
#
#  __init__.py
"""
Docstring Goes Here
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
import os
import pathlib
from typing import Iterable, Optional, Union

# this package
from .templates import templates

__all__ = ["make_document"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "MIT License"
__version__ = "0.0.6"
__email__ = "dominic@davis-foster.co.uk"

main_template = templates.get_template("main.tex")


def make_document(
		outfile: Union[str, pathlib.Path, os.PathLike],
		elements: Optional[Iterable[str]] = None,
		glossary: str = '',
		):

	if not isinstance(outfile, pathlib.Path):
		outfile = pathlib.Path(outfile)

	if elements is None:
		elements = []

	with open(outfile, 'w') as fp:
		fp.write(main_template.render(elements=elements, glossary=glossary))
