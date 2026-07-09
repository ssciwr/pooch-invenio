# Welcome to doiggie-invenio

[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/doiggie-invenio/ci.yml?branch=main)](https://github.com/ssciwr/doiggie-invenio/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ssciwr/doiggie-invenio/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/doiggie-invenio)

`doiggie-invenio` adds support for the [InvenioRDM data repository software](https://inveniosoftware.org/products/rdm/)
to the [doiggie](https://github.com/ssciwr/doiggie) ecosystem. As InvenioRDM is the software powering Zenodo,
this repository implicitly also contains the support for Zenodo.

## Installation

The Python package `doiggie-invenio` can be installed from PyPI:

```
python -m pip install doiggie-invenio
```

If you want to install all available data repository implementations for `doiggie`,
consider install [doiggie-repositories](https://github.com/ssciwr/doiggie-repositories) instead.

## Known Issues

Zenodo has recently (writing February 2026) implemented drastic rate limiting, presumably
due to abusive usage by AI web crawlers. We try to address this issue, but have limited
agency to do so. For a discussion of the issue, please have a look at [this upstream issue](https://github.com/fatiando/pooch/issues/502).
