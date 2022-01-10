# National Road Network (NRN)
[![GitHub license](https://img.shields.io/github/license/jessestewart1/nrn-rrn)](https://github.com/jessestewart1/nrn-rrn/blob/master/LICENSE.rst)
[![Documentation Status](https://readthedocs.org/projects/nrn-rrn-docs/badge/?version=latest;style=flat)](https://nrn-rrn-docs.readthedocs.io/en/latest/?badge=latest)

## Contents:

- [Description](#description)
- [Setup](#setup)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)

## Description

The NRN was adopted by members from the Inter-Agency Committee on Geomatics (IACG) and the Canadian Council on 
Geomatics (CCOG) to provide quality geospatial and attributive data (current, accurate, consistent), homogeneous and 
normalized of the entire Canadian road network. The NRN is part of the GeoBase initiative which aims to provide a 
common geospatial infrastructure that is maintained on a regular basis by closest to source organizations.

The NRN is distributed in the form of thirteen provincial / territorial datasets consisting of two linear entities 
(road segments and ferry segments), three punctual entities (junctions, blocked passages, and toll points), and three
tabular entities (address ranges, street and place names, and alternative name linkages). Currently, the NRN is 
publicly available on the open government data portal (https://open.canada.ca/en).

The NRN content largely conforms to ISO 14825 (https://www.iso.org/standard/54610.html).

## Setup

The NRN is written in pure Python, but has several dependencies written in C. These dependencies can often be difficult 
to install and, therefore, it is recommended to create and use the `conda` environment defined in the NRN repository.

### Prerequisites

The only prerequisite is Anaconda with `conda` >= 4.9 (the latest version of Anaconda will satisfy this requirement).
Anaconda can be downloaded from: https://docs.anaconda.com/anaconda/install/.

Once installed, the `conda` version can be validated in the command line with:
```
conda -V
```

### Installation

FIX THIS SECTION

1. Download and unzip the repository: https://github.com/jessestewart1/nrn-rrn

2. Create a virtual conda environment from the file `environment.yml`:

   `conda env create -f <path to environment.yml>`

3. Validate the successful creation of the virtual environment by listing all available environments:

   `conda env list`
