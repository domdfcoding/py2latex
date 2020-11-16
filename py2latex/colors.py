#!/usr/bin/env python
#
#  colors.py
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

__all__ = [
		"black",
		"blue",
		"brown",
		"colour",
		"cyan",
		"darkgray",
		"darkgrey",
		"gray",
		"green",
		"grey",
		"lime",
		"magenta",
		"olive",
		"orange",
		"pink",
		"purple",
		"red",
		"teal",
		"violet",
		"white",
		"yellow"
		]


def colour(text_colour: str, text: str):
	r"""Make the given text the given colour

	Akin to \color{text_colour}{string}

	:param text_colour: The colour to make the text
	:param text: The text to colour

	:return: The formatted string.
	"""

	return fr"{{\color{{{text_colour}}}{text}}}"


def black(text: str):
	r"""Make the given text black

	Akin to \color{black}{string}

	:param text: The text to make black

	:return: The formatted string.
	"""

	return colour("black", text)


def blue(text: str):
	r"""Make the given text blue

	Akin to \color{blue}{string}

	:param text: The text to make blue

	:return: The formatted string.
	"""

	return colour("blue", text)


def brown(text: str):
	r"""Make the given text brown

	Akin to \color{brown}{string}

	:param text: The text to make brown

	:return: The formatted string.
	"""

	return colour("brown", text)


def cyan(text: str):
	r"""Make the given text cyan

	Akin to \color{cyan}{string}

	:param text: The text to make cyan

	:return: The formatted string.
	"""

	return colour("cyan", text)


def darkgrey(text: str):
	r"""Make the given text darkgrey

	Akin to \color{darkgray}{string}

	:param text: The text to make darkgrey

	:return: The formatted string.
	"""

	return colour("darkgray", text)


def darkgray(text: str):
	r"""Make the given text darkgray

	Akin to \\color{darkgray}{string}

	:param text: The text to make darkgray

	:return: The formatted string.
	"""

	return colour("darkgray", text)


def grey(text: str):
	r"""Make the given text grey

	Akin to \color{gray}{string}

	:param text: The text to make grey

	:return: The formatted string.
	"""

	return colour("gray", text)


def gray(text: str):
	r"""Make the given text gray

	Akin to \color{gray}{string}

	:param text: The text to make gray

	:return: The formatted string.
	"""

	return colour("gray", text)


def green(text: str):
	r"""Make the given text green

	Akin to \color{green}{string}

	:param text: The text to make green

	:return: The formatted string.
	"""

	return colour("green", text)


def lime(text: str):
	r"""Make the given text lime

	Akin to \color{lime}{string}

	:param text: The text to make lime

	:return: The formatted string.
	"""

	return colour("lime", text)


def magenta(text: str):
	r"""Make the given text magenta

	Akin to \color{magenta}{string}

	:param text: The text to make magenta

	:return: The formatted string.
	"""

	return colour("magenta", text)


def olive(text: str):
	r"""Make the given text olive

	Akin to \color{olive}{string}

	:param text: The text to make olive

	:return: The formatted string.
	"""

	return colour("olive", text)


def orange(text: str):
	r"""Make the given text orange

	Akin to \color{orange}{string}

	:param text: The text to make orange

	:return: The formatted string.
	"""

	return colour("orange", text)


def pink(text: str):
	r"""Make the given text pink

	Akin to \color{pink}{string}

	:param text: The text to make pink

	:return: The formatted string.
	"""

	return colour("pink", text)


def purple(text: str):
	r"""Make the given text purple

	Akin to \color{purple}{string}

	:param text: The text to make purple

	:return: The formatted string.
	"""

	return colour("purple", text)


def red(text: str):
	r"""Make the given text red

	Akin to \color{red}{string}

	:param text: The text to make red

	:return: The formatted string.
	"""

	return colour("red", text)


def teal(text: str):
	r"""Make the given text teal

	Akin to \color{teal}{string}

	:param text: The text to make teal

	:return: The formatted string.
	"""

	return colour("teal", text)


def violet(text: str):
	r"""Make the given text violet

	Akin to \color{violet}{string}

	:param text: The text to make violet

	:return: The formatted string.
	"""

	return colour("violet", text)


def white(text: str):
	r"""Make the given text white

	Akin to \color{white}{string}

	:param text: The text to make white

	:return: The formatted string.
	"""

	return colour("white", text)


def yellow(text: str):
	r"""Make the given text yellow

	Akin to \color{yellow}{string}

	:param text: The text to make yellow

	:return: The formatted string.
	"""

	return colour("yellow", text)
