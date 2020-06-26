#  !/usr/bin/env python
#
#  siunit.py
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
from typing import List

import astropy.units as u
from typing_extensions import Literal


siunitx_abbreviations = {
		# abbreviation, symbol  # unit
		"fg": r"\fg",  # femtogram
		"pg": r"\pg",  # picogram
		"ng": r"\ng",  # nanogram
		"µg": r"\ug",  # microgram
		"mg": r"\mg",  # milligram
		"g": r"\g",  # gram
		"kg": r"\kg",  # kilogram
		"u": r"\amu",  # atomic mass unit
		"pm": r"\pm",  # picometre
		"nm": r"\nm",  # nanometre
		"µm": r"\um",  # micrometre
		"mm": r"\mm",  # millimetre
		"cm": r"\cm",  # centimetre
		"dm": r"\dm",  # decimetre
		"m": r"\m",  # metre
		"km": r"\km",  # kilometre
		"as": r"\as",  # attosecond
		"fs": r"\fs",  # femtosecond
		"ps": r"\ps",  # picosecond
		"ns": r"\ns",  # nanosecond
		"µs": r"\us",  # microsecond
		"ms": r"\ms",  # millisecond
		"s": r"\s",  # second
		"fmol": r"\fmol",  # femtomole
		"pmol": r"\pmol",  # picomole
		"nmol": r"\nmol",  # nanomole
		"µmol": r"\umol",  # micromole
		"mmol": r"\mmol",  # millimole
		"mol": r"\mol",  # mole
		"kmol": r"\kmol",  # kilomole
		"pA": r"\pA",  # picoampere
		"nA": r"\nA",  # nanoampere
		"µA": r"\uA",  # microampere
		"mA": r"\mA",  # milliampere
		"A": r"\A",  # ampere
		"kA": r"\kA",  # kiloampere
		"µl": r"\ul",  # microlitre
		"ml": r"\ml",  # millilitre
		"l": r"\l",  # litre
		"hl": r"\hl",  # hectolitre
		"µL": r"\uL",  # microliter
		"mL": r"\mL",  # milliliter
		"L": r"\L",  # liter
		"hL": r"\hL",  # hectoliter
		"mHz": r"\mHz",  # millihertz
		"Hz": r"\Hz",  # hertz
		"kHz": r"\kHz",  # kilohertz
		"MHz": r"\MHz",  # megahertz
		"GHz": r"\GHz",  # gigahertz
		"THz": r"\THz",  # terahertz
		"mN": r"\mN",  # millinewton
		"N": r"\N",  # newton
		"kN": r"\kN",  # kilonewton
		"MN": r"\MN",  # meganewton
		"Pa": r"\Pa",  # pascal
		"kPa": r"\kPa",  # kilopascal
		"MPa": r"\MPa",  # megapacal
		"GPa": r"\GPa",  # gigapascal
		"mΩ": r"\mohm",  # milliohm
		"kΩ": r"\kohm",  # kilohm
		"MΩ": r"\Mohm",  # megohm
		"pV": r"\pV",  # picovolt
		"nV": r"\nV",  # nanovolt
		"µV": r"\uV",  # microvolt
		"mV": r"\mV",  # millivolt
		"V": r"\V",  # volt
		"kV": r"\kV",  # kilovolt
		"W": r"\W",  # watt
		"µW": r"\uW",  # microwatt
		"mW": r"\mW",  # milliwatt
		"kW": r"\kW",  # kilowatt
		"MW": r"\MW",  # megawatt
		"GW": r"\GW",  # gigawatt
		"J": r"\J",  # joule
		"µJ": r"\uJ",  # microjoule
		"mJ": r"\mJ",  # millijoule
		"kJ": r"\kJ",  # kilojoule
		"eV": r"\eV",  # electronvolt
		"meV": r"\meV",  # millielectronvolt
		"keV": r"\keV",  # kiloelectronvolt
		"MeV": r"\MeV",  # megaelectronvolt
		"GeV": r"\GeV",  # gigaelectronvolt
		"TeV": r"\TeV",  # teraelectronvolt
		"kWh": r"\kWh",  # kilowatt hour
		"F": r"\F",  # farad
		"fF": r"\fF",  # femtofarad
		"pF": r"\pF",  # picofarad
		"K": r"\K",  # kelvin
		"dB": r"\dB",  # decibel
		"T": r"\tesla",  # tesla
		"lx": r"\lux",  # lux
		}


def get_si_elements(unit: u.UnitBase) -> List[str]:

	elems = []

	for base, power in zip(unit.bases, unit.powers):

		if str(base) in siunitx_abbreviations:
			base = siunitx_abbreviations[str(base)]

		# print(base, power)
		if power > 1:
			elems.append(rf"{base}\tothe{{{power}}}")
		elif power < 0:
			elems.append(rf"\per{base}\tothe{{{abs(power)}}}")
		else:
			elems.append(str(base))

	return elems


def si(
		unit: u.UnitBase,
		per_mode: Literal["repeated-symbol", "symbol", "fraction", "symbol-or-fraction", "reciprocal"] = "symbol",
		) -> str:
	"""
	Create an siunitx-formatted formula from an `astropy.units <https://docs.astropy.org/en/stable/units/>`_ unit.

	:param unit:
	:param per_mode:

	:return:
	:rtype: str
	"""

	elems = get_si_elements(unit)

	return rf"\si[per-mode={per_mode}]{{{' '.join(elems)}}}"



def SI(
		quantity: u.Quantity,
		per_mode: Literal["repeated-symbol", "symbol", "fraction", "symbol-or-fraction", "reciprocal"] = "symbol",
		) -> str:
	"""
	Create an siunitx-formatted formula from an `astropy.units <https://docs.astropy.org/en/stable/units/>`_ unit.

	:param quantity:
	:param per_mode:

	:return:
	:rtype: str
	"""

	unit = quantity.unit
	value = quantity.value
	elems = get_si_elements(unit)

	return rf"\SI[per-mode={per_mode}]{{{value}}}{{{' '.join(elems)}}}"


if __name__ == '__main__':

	kgms = u.kg * u.m * u.s**-1
	print(si(kgms))

	kgmAs = u.kg * u.m /u.A / u.s
	print(si(kgmAs))

	l3vt3 = u.lux**3 * u.V / u.T ** 3
	print(si(l3vt3))

	print(3* l3vt3)

	print((3* l3vt3).value)
	print((3* l3vt3).unit)
