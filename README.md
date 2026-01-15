# Welcome to pooch-invenio

[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/pooch-invenio/ci.yml?branch=main)](https://github.com/ssciwr/pooch-invenio/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/pooch-invenio/badge/)](https://pooch-invenio.readthedocs.io/)
[![codecov](https://codecov.io/gh/ssciwr/pooch-invenio/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/pooch-invenio)

## Installation

The Python package `pooch_invenio` can be installed from PyPI:

```
python -m pip install pooch_invenio
```

## Development installation

If you want to contribute to the development of `pooch_invenio`, we recommend
the following editable installation from this repository:

```
git clone git@github.com:ssciwr/pooch-invenio.git
cd pooch-invenio
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
