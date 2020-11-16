#!/usr/bin/env python
#
#  glossaries.py
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
import os
import pathlib
from typing import Dict, Union

# 3rd party
import yaml

# this package
from py2latex.markdown_parser import parse_markdown

__all__ = ["escape_prefix", "glossary_from_file", "load_glossary", "make_glossary"]


def load_glossary(glossary_file: Union[str, pathlib.Path, os.PathLike]) -> Dict[str, Dict[str, str]]:
	if not isinstance(glossary_file, pathlib.Path):
		glossary_file = pathlib.Path(glossary_file)

	# todo: Validate

	with glossary_file.open() as fp:
		glossary = yaml.load(fp, Loader=yaml.FullLoader)

	for entry, data in glossary["acronyms"].items():
		data["name"] = parse_markdown(data["name"]).strip()
		data["text"] = parse_markdown(data["text"]).strip()

	for entry, data in glossary["glossary"].items():
		data["name"] = parse_markdown(data["name"]).strip()
		data["text"] = parse_markdown(data["text"]).strip()
		data["description"] = parse_markdown(data["description"]).strip()

	return glossary


def escape_prefix(prefix: str) -> str:
	prefix = prefix.replace(' ', "\\ ")
	return prefix


def make_glossary(glossary_dict):
	out = ''

	for acronym, data in glossary_dict["acronyms"].items():
		out += r"\newacronym"

		prefixes = []

		if "prefixfirst" in data:
			prefixes.append(f"prefixfirst={{{escape_prefix(data['prefixfirst'])}}}")
		if "prefix" in data:
			prefixes.append(f"prefix={{{escape_prefix(data['prefix'])}}}")

		if prefixes:
			out += f"[{', '.join(prefixes)}]"

		out += f"{{{acronym}}}{{{data['name']}}}{{{data['text']}}}\n"

	for item, data in glossary_dict["glossary"].items():
		out += fr"""
\newglossaryentry{{{item}}}
{{
name={{{data['name']}}},
text={{{data['text']}}},
description={{{data['description']}}},
}}"""
	return out


def glossary_from_file(filename):
	return make_glossary(load_glossary(filename))
