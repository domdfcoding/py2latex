#!/usr/bin/env python3
# From https://github.com/rufuspollock/markdown2latex
# BSD Licensed
"""
Extension to python-markdown to support LaTeX (rather than html) output.

Authored by Rufus Pollock: <http://www.rufuspollock.org/>
Reworked by Julian Wulfheide (ju.wulfheide@gmail.com) and
Pedro Gaudencio (pmgaudencio@gmail.com)

Usage:
======

1. As a python-markdown extension::

	>>> import markdown
	>>> md = markdown.Markdown(None, extensions=['latex'])
	>>> # text is input string ...
	>>> latex_out = md.convert(text)

2. Directly as a module (slight inversion of std markdown extension setup)::

	>>> import markdown
	>>> import mdx_latex
	>>> md = markdown.Markdown()
	>>> latex_mdx = mdx_latex.LaTeXExtension()
	>>> latex_mdx.extendMarkdown(md, markdown.__dict__)
	>>> out = md.convert(text)

History
=======

Version: 1.0 (November 15, 2006)

* First working version (compatible with markdown 1.5)
* Includes support for tables

Version: 1.1 (January 17, 2007)

* Support for verbatim and images

Version: 1.2 (June 2008)

* Refactor as an extension.
* Make into a proper python/setuptools package.
* Tested with markdown 1.7 but should work with 1.6 and (possibly) 1.5
	(though pre/post processor stuff not as worked out there)

Version 1.3: (July 2008)
* Improvements to image output (width)

Version 1.3.1: (August 2009)
* Tiny bugfix to remove duplicate keyword argument and set zip_safe=False
* Add [width=\textwidth] by default for included images

Version 2.0: (June 2011)
* PEP8 cleanup
* Major rework since this was broken by new Python-Markdown releases

Version 2.1: (August 2013)
* Add handler for non locally referenced images, hyperlinks and horizontal rules
* Update math delimiters
"""

# stdlib
import re

# 3rd party
import markdown  # type: ignore


def makeExtension(configs=None):
	return LaTeXExtension(configs=configs)


"""
========================= FOOTNOTES =================================

LaTeX footnote support.

Implemented via modification of original markdown approach (place footnote
definition in footnote market <sup> as opposed to putting a reference link).
"""


class FootnoteExtension(markdown.Extension):
	DEF_RE = re.compile(r"( ? ? ?)\[\^([^\]]*)\]:\s*(.*)")
	SHORT_USE_RE = re.compile(r"\[\^([^\]]*)\]", re.M)  # [^a]

	def __init__(self, **kwargs):
		self.reset()
		super().__init__(**kwargs)

	def extendMarkdown(self, md, md_globals):
		self.md = md

		# Stateless extensions do not need to be registered
		md.registerExtension(self)

		# Insert a preprocessor before ReferencePreprocessor
		# index = md.preprocessors.index(md_globals['REFERENCE_PREPROCESSOR'])
		# preprocessor = FootnotePreprocessor(self)
		# preprocessor.md = md
		# md.preprocessors.insert(index, preprocessor)
		md.preprocessors.add("footnotes", FootnotePreprocessor(self), "_begin")

		# Insert an inline pattern before ImageReferencePattern
		FOOTNOTE_RE = r"\[\^([^\]]*)\]"  # blah blah [^1] blah
		# index = md.inlinePatterns.index(md_globals['IMAGE_REFERENCE_PATTERN'])
		# md.inlinePatterns.insert(index, FootnotePattern(FOOTNOTE_RE, self))
		md.inlinePatterns.add("footnotes", FootnotePattern(FOOTNOTE_RE, self), "_begin")

	def reset(self):
		self.used_footnotes = {}
		self.footnotes = {}

	def setFootnote(self, id, text):
		self.footnotes[id] = text


class FootnotePreprocessor:

	def __init__(self, footnotes):
		self.footnotes = footnotes

	def run(self, lines):
		self.blockGuru = BlockGuru()
		lines = self._handleFootnoteDefinitions(lines)

		# Make a hash of all footnote marks in the text so that we
		# know in what order they are supposed to appear.  (This
		# function call doesn't really substitute anything - it's just
		# a way to get a callback for each occurence.

		text = '\n'.join(lines)
		self.footnotes.SHORT_USE_RE.sub(self.recordFootnoteUse, text)

		return text.split('\n')

	def recordFootnoteUse(self, match):
		id = match.group(1)
		id = id.strip()
		nextNum = len(list(self.footnotes.used_footnotes.keys())) + 1
		self.footnotes.used_footnotes[id] = nextNum

	def _handleFootnoteDefinitions(self, lines):
		"""
		Recursively finds all footnote definitions in the lines.

		:param lines: a list of lines of text
		:return: a string representing the text with footnote definitions removed
		"""

		i, id, footnote = self._findFootnoteDefinition(lines)

		if id:

			plain = lines[:i]

			detabbed, theRest = self.blockGuru.detectTabbed(lines[i + 1:])

			self.footnotes.setFootnote(id, footnote + '\n' + '\n'.join(detabbed))

			more_plain = self._handleFootnoteDefinitions(theRest)
			return plain + [''] + more_plain

		else:
			return lines

	def _findFootnoteDefinition(self, lines):
		"""
		Finds the first line of a footnote definition.

		:param lines: a list of lines of text
		:return: the index of the line containing a footnote definition.
		"""

		counter = 0
		for line in lines:
			m = self.footnotes.DEF_RE.match(line)
			if m:
				return counter, m.group(2), m.group(3)
			counter += 1
		return counter, None, None


class FootnotePattern(markdown.inlinepatterns.Pattern):

	def __init__(self, pattern, footnotes):
		markdown.inlinepatterns.Pattern.__init__(self, pattern)
		self.footnotes = footnotes

	def handleMatch(self, m, doc):
		sup = doc.createElement("sup")
		id = m.group(2)
		# stick the footnote text in the sup
		self.footnotes.md._processSection(sup, self.footnotes.footnotes[id].split('\n'))
		return sup


def template(template_fo, latex_to_insert):
	tmpl = template_fo.read()
	tmpl = tmpl.replace("INSERT-TEXT-HERE", latex_to_insert)
	return tmpl


# title_items = [ '\\title', '\\end{abstract}', '\\thanks', '\\author' ]
# has_title_stuff = False
# for it in title_items:
#    has_title_stuff = has_title_stuff or (it in tmpl)
