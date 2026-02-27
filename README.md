# Welcome to pooch-invenio

[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/pooch-invenio/ci.yml?branch=main)](https://github.com/ssciwr/pooch-invenio/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ssciwr/pooch-invenio/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/pooch-invenio)

`pooch-invenio` adds support for the [InvenioRDM data repository software](https://inveniosoftware.org/products/rdm/)
to the [pooch-doi](https://github.com/ssciwr/pooch-doi) ecosystem. As InvenioRDM is the software powering Zenodo,
this repository implicitly also contains the support for Zenodo.

## Installation

The Python package `pooch_invenio` can be installed from PyPI:

```
python -m pip install pooch_invenio
```

If you want to install all available data repository implementations for `pooch-doi`,
consider install [pooch-repositories](https://github.com/ssciwr/pooch-repositories) instead.

## Known Issues

Zenodo has recently (writing February 2026) implemented drastic rate limiting, presumably
due to abusive usage by AI web crawlers. We try to address this issue, but have limited
agency to do so. For a discussion of the issue, please have a look at [this upstream issue](https://github.com/fatiando/pooch/issues/502).
