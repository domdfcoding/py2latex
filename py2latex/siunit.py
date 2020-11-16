#!/usr/bin/env python
#
#  siunit.py
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
from typing import List

# 3rd party
from astropy.units import (  # type: ignore
		GW,
		MN,
		MW,
		GeV,
		GHz,
		GPa,
		MeV,
		MHz,
		Mohm,
		MPa,
		Quantity,
		TeV,
		THz,
		UnitBase,
		cm,
		dm,
		fF,
		fmol,
		fs,
		hL,
		kA,
		keV,
		kHz,
		kJ,
		km,
		kmol,
		kN,
		kohm,
		kPa,
		kV,
		kW,
		mA,
		meV,
		mHz,
		mJ,
		mL,
		mm,
		mmol,
		mN,
		mohm,
		ms,
		mV,
		mW,
		nA,
		nm,
		nmol,
		ns,
		nV,
		pA,
		pF,
		pmol,
		ps,
		pV,
		uA,
		uJ,
		uL,
		um,
		umol,
		us,
		uV,
		uW
		)
from astropy.units.astrophys import AU, M_e, astronomical_unit, au, u  # type: ignore
from astropy.units.cds import mmHg  # type: ignore; type: ignore
from astropy.units.cds import bar, barn
from astropy.units.cds import c as clight
from astropy.units.cds import e as elementarycharge
from astropy.units.imperial import knot, nauticalmile  # type: ignore
from astropy.units.si import (  # type: ignore
		A,
		Bq,
		C,
		Celsius,
		F,
		H,
		Hz,
		J,
		K,
		Kelvin,
		L,
		N,
		Pa,
		S,
		T,
		V,
		W,
		Wb,
		ampere,
		angstrom,
		arcmin,
		arcminute,
		arcsec,
		arcsecond,
		becquerel,
		candela,
		cd,
		coulomb,
		d,
		day,
		deg,
		deg_C,
		degree,
		eV,
		farad,
		fg,
		g,
		h,
		henry,
		hertz,
		hour,
		joule,
		kg,
		kilogram,
		liter,
		lm,
		lumen,
		lux,
		lx,
		m,
		meter,
		mg,
		min,
		minute,
		mol,
		mole,
		newton,
		ng,
		ohm,
		pascal,
		pg,
		pm,
		rad,
		radian,
		s,
		second,
		siemens,
		sr,
		steradian,
		t,
		tesla,
		tonne,
		ug,
		volt,
		watt,
		weber
		)
from typing_extensions import Literal

kelvin = Kelvin
metre = meter
degreeCelsius = deg_C
astronomicalunit = astronomical_unit
atomicmassunit = u
electronmass = M_e
electronvolt = eV

# TODO: litre, l
# TODO hectare, ha
# TODO: sievert, Sv
# todo: katal, kat
# TODO: gray, Gy
# TODO distinguish dalton, Da from amu
# TODO: bohr
# TODO as lowercase l: ul, ml, hl,
# 		"as": r"\as",  # attosecond
# TODO: bel & decibel, dB
# TODO hartree
# TODO: reduced Planck constant
# TODO neper
# TODO SI prefixes
# TODO kWh

__all__ = ["SI", "get_si_elements", "si"]

siunitx_abbreviations = {
		# abbreviation, symbol  # unit
		"fg": r"\fg",  # femtogram
		"pg": r"\pg",  # picogram
		"ng": r"\ng",  # nanogram
		"µg": r"\ug",  # microgram
		"mg": r"\mg",  # milligram
		'g': r"\g",  # gram
		"kg": r"\kg",  # kilogram
		'u': r"\amu",  # atomic mass unit
		"pm": r"\pm",  # picometre
		"nm": r"\nm",  # nanometre
		"µm": r"\um",  # micrometre
		"mm": r"\mm",  # millimetre
		"cm": r"\cm",  # centimetre
		"dm": r"\dm",  # decimetre
		'm': r"\m",  # metre
		"km": r"\km",  # kilometre
		"as": r"\as",  # attosecond
		"fs": r"\fs",  # femtosecond
		"ps": r"\ps",  # picosecond
		"ns": r"\ns",  # nanosecond
		"µs": r"\us",  # microsecond
		"ms": r"\ms",  # millisecond
		's': r"\s",  # second
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
		'A': r"\A",  # ampere
		"kA": r"\kA",  # kiloampere
		"µl": r"\ul",  # microlitre
		"ml": r"\ml",  # millilitre
		'l': r"\l",  # litre
		"hl": r"\hl",  # hectolitre
		"µL": r"\uL",  # microliter
		"mL": r"\mL",  # milliliter
		'L': r"\L",  # liter
		"hL": r"\hL",  # hectoliter
		"mHz": r"\mHz",  # millihertz
		"Hz": r"\Hz",  # hertz
		"kHz": r"\kHz",  # kilohertz
		"MHz": r"\MHz",  # megahertz
		"GHz": r"\GHz",  # gigahertz
		"THz": r"\THz",  # terahertz
		"mN": r"\mN",  # millinewton
		'N': r"\N",  # newton
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
		'V': r"\V",  # volt
		"kV": r"\kV",  # kilovolt
		'W': r"\W",  # watt
		"µW": r"\uW",  # microwatt
		"mW": r"\mW",  # milliwatt
		"kW": r"\kW",  # kilowatt
		"MW": r"\MW",  # megawatt
		"GW": r"\GW",  # gigawatt
		'J': r"\J",  # joule
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
		'F': r"\F",  # farad
		"fF": r"\fF",  # femtofarad
		"pF": r"\pF",  # picofarad
		'K': r"\K",  # kelvin
		"dB": r"\dB",  # decibel
		'T': r"\tesla",  # tesla
		"lx": r"\lux",  # lux
		}

astropy_siunitx_mapping = {
		ampere: r"\ampere",
		A: r"\ampere",
		candela: r"\candela",
		cd: r"\candela",
		kelvin: r"\kelvin",
		Kelvin: r"\kelvin",
		K: r"\kelvin",
		kilogram: r"\kilogram",
		kg: r"\kilogram",
		meter: r"\metre",
		metre: r"\metre",
		m: r"\metre",
		mole: r"\mole",
		mol: r"\mole",
		second: r"\second",
		s: r"\second",
		deg_C: r"\degreeCelsius",
		Celsius: r"\degreeCelsius",
		degreeCelsius: r"\degreeCelsius",
		coulomb: r"\coulomb",
		C: r"\coulomb",
		farad: r"\farad",
		F: r"\farad",  # TODO: gray, Gy
		hertz: r"\hertz",
		Hz: r"\hertz",
		henry: r"\henry",
		H: r"\henry",
		joule: r"\joule",
		J: r"\joule",  # todo: katal, kat
		lumen: r"\lumen",
		lm: r"\lumen",
		lux: r"\lux",
		lx: r"\lux",
		newton: r"\newton",
		N: r"\newton",
		ohm: r"\ohm",
		pascal: r"\pascal",
		Pa: r"\pascal",
		radian: r"\radian",
		rad: r"\radian",
		siemens: r"\siemens",
		S: r"\siemens",  # TODO: sievert, Sv
		steradian: r"\steradian",
		sr: r"\steradian",
		tesla: r"\tesla",
		T: r"\tesla",
		volt: r"\volt",
		V: r"\volt",
		watt: r"\watt",
		W: r"\watt",
		weber: r"\weber",
		Wb: r"\weber",
		day: r"\day",
		d: r"\day",
		degree: r"\degree",
		deg: r"\degree",  # TODO hectare, ha
		hour: r"\hour",
		h: r"\hour",
		liter: r"\liter",
		L: r"\liter",  # TODO: litre, l
		arcminute: r"\arcminute",
		arcmin: r"\arcminute",
		minute: r"\minute",
		min: r"\minute",
		arcsecond: r"\arcsecond",
		arcsec: r"\arcsecond",
		tonne: r"\tonne",
		t: r"\tonne",
		astronomical_unit: r"\astronomicalunit",
		AU: r"\astronomicalunit",
		au: r"\astronomicalunit",
		astronomicalunit: r"\astronomicalunit",  # TODO: bohr
		clight: r"\clight",  # TODO distinguish dalton, Da from amu
		M_e: r"\electronmass",
		electronmass: r"\electronmass",
		eV: r"\electronvolt",
		electronvolt: r"\electronvolt",
		elementarycharge: r"\elementarycharge",  # TODO hartree
		# TODO: reduced Planck constant
		angstrom: r"\angstrom",
		bar: r"\bar",
		barn: r"\barn",  # TODO: bel & decibel, dB
		knot: r"\knot",
		mmHg: r"\mmHg",
		nauticalmile: r"\nauticalmile",  # TODO neper
		g: r"\g",
		fg: r"\fg",
		pg: r"\pg",
		ng: r"\ng",
		ug: r"\ug",
		mg: r"\mg",
		pm: r"\pm",
		nm: r"\nm",
		um: r"\um",
		mm: r"\mm",
		cm: r"\cm",
		dm: r"\dm",
		km: r"\km",
		fs: r"\fs",
		ps: r"\ps",
		ns: r"\ns",
		us: r"\us",
		ms: r"\ms",
		fmol: r"\fmol",
		pA: r"\pA",
		uL: r"\uL",
		mHz: r"\mHz",
		mN: r"\mN",
		kPa: r"\kPa",
		mohm: r"\mohm",
		pV: r"\pV",
		uW: r"\uW",
		uJ: r"\uJ",
		meV: r"\meV",
		pmol: r"\pmol",
		nmol: r"\nmol",
		umol: r"\umol",
		mmol: r"\mmol",
		kmol: r"\kmol",
		nA: r"\nA",
		uA: r"\uA",
		mA: r"\mA",
		kA: r"\kA",
		mL: r"\mL",
		hL: r"\hL",
		kHz: r"\kHz",
		MHz: r"\MHz",
		GHz: r"\GHz",
		THz: r"\THz",
		kN: r"\kN",
		MN: r"\MN",
		MPa: r"\MPa",
		GPa: r"\GPa",
		kohm: r"\kohm",
		Mohm: r"\Mohm",
		nV: r"\nV",
		uV: r"\uV",
		mV: r"\mV",
		kV: r"\kV",
		mW: r"\mW",
		kW: r"\kW",
		MW: r"\MW",
		GW: r"\GW",
		mJ: r"\mJ",
		kJ: r"\kJ",
		keV: r"\keV",
		MeV: r"\MeV",
		GeV: r"\GeV",
		TeV: r"\TeV",
		fF: r"\fF",
		pF: r"\pF",
		}


def get_si_elements(unit: UnitBase) -> List[str]:

	elems = []

	for base, power in zip(unit.bases, unit.powers):

		if base in astropy_siunitx_mapping:
			print(base)
			base = astropy_siunitx_mapping[base]

		# print(base, power)
		if power > 1:
			elems.append(rf"{base}\tothe{{{power}}}")
		elif power < 0:
			elems.append(rf"\per{base}\tothe{{{abs(power)}}}")
		else:
			elems.append(str(base))

	return elems


def si(
		unit: UnitBase,
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
		quantity: Quantity,
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


if __name__ == "__main__":

	kgms = kg * m * s**-1
	print(si(kgms))

	kgmAs = kg * m / A / s
	print(si(kgmAs))

	l3vt3 = lux**3 * V / T**3
	print(si(l3vt3))

	print(3 * l3vt3)

	print((3 * l3vt3).value)
	print((3 * l3vt3).unit)

	print(si(mg / L))
