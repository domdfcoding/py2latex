#########
py2LaTeX
#########

.. start short_desc

**Create LaTeX documents with Python, Markdown and Jinja2.**

.. end short_desc

This project is at a VERY early stage, and as such things might not work and WILL break between versions.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/py2latex/latest?logo=read-the-docs
	:target: https://py2latex.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/py2latex/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/py2latex/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/py2latex/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/py2latex/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/py2latex/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/py2latex/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/py2latex/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/py2latex/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/py2latex/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/py2latex?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/py2latex
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/py2latex
	:target: https://pypi.org/project/py2latex/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py2latex?logo=python&logoColor=white
	:target: https://pypi.org/project/py2latex/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py2latex
	:target: https://pypi.org/project/py2latex/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/py2latex
	:target: https://pypi.org/project/py2latex/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/py2latex
	:target: https://github.com/domdfcoding/py2latex/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/py2latex
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/py2latex/v0.0.6
	:target: https://github.com/domdfcoding/py2latex/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/py2latex
	:target: https://github.com/domdfcoding/py2latex/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/py2latex
	:target: https://pypi.org/project/py2latex/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/py2latex/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/py2latex/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``py2LaTeX`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install py2latex

.. end installation
