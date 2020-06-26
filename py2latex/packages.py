#  !/usr/bin/env python
#
#  packages.py
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
from typing import List, Optional


def usepackage(package_name: str, options: Optional[str] = None) -> str:
	r"""

	Akin to \usepackage[options]{package_name}

	:param package_name: The name of the package
	:param options: Options for the package

	:return:
	"""

	if options:
		return rf"\usepackage[{options}]{{{package_name}}}"
	else:
		return rf"\usepackage{{{package_name}}}"


class PackageTracker:

	packages: List[str] = []

	@classmethod
	def requires(cls, package: str):
		if package not in cls.packages:
			cls.packages.append(package)

		def wrap(f):

			def wrapped_f(*args, **kwargs):
				f(*args, **kwargs)

			return wrapped_f

		return wrap


# @PackageTracker.requires("xcolor")
# def foo():
# 	print("inside foo!")

# print(PackageTracker.packages)
