#!/usr/bin/env python
#
#  packages.py
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
from typing import Callable, List, Optional, Set, Type

__all__ = ["PackageTracker", "usepackage"]


def usepackage(package_name: str, options: Optional[str] = None) -> str:
	r"""
	Akin to ``\usepackage[options]{package_name}``.

	:param package_name: The name of the package
	:param options: Options for the package
	"""

	if options:
		return rf"\usepackage[{options}]{{{package_name}}}"
	else:
		return rf"\usepackage{{{package_name}}}"


class PackageTracker:

	packages: Set[str] = set()

	def __new__(cls: Type["PackageTracker"]) -> Type["PackageTracker"]:  # type: ignore[misc]
		return cls

	@classmethod
	def requires(cls, package: str) -> Callable[[Callable], Callable]:
		"""
		Mark a function as requiring a particular package when invoked.

		:param package:
		"""

		def wrap(f: Callable) -> Callable:

			def wrapped_f(*args, **kwargs):
				cls.packages.add(package)
				f(*args, **kwargs)

			return wrapped_f

		return wrap


# @PackageTracker.requires("xcolor")
# def foo():
# 	print("inside foo!")

# print(PackageTracker.packages)
