# stdlib
import os
import pathlib
import re
from typing import Dict, Union

# 3rd party
import yaml

# this package
from py2latex.markdown_parser import parse_markdown


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
	prefix = prefix.replace(" ", "\\ ")
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
