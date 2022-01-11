# National Road Network (NRN)
[![Repository](https://img.shields.io/badge/Repository-nrn--rrn-brightgreen.svg?style=flat-square&logo=github)](https://github.com/jessestewart1/nrn-rrn)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://opensource.org/licenses/BSD-3-Clause)
[![Documentation Status](https://readthedocs.org/projects/nrn-rrn-docs/badge/?style=flat-square)](https://nrn-rrn-docs.readthedocs.io/en/latest/)

## Contents:

- [Description](#description)
- [Setup](#setup)
  * [Software Dependencies](#software-dependencies)
  * [Installation](#installation)

## Description

The NRN was adopted by members from the Inter-Agency Committee on Geomatics (IACG) and the Canadian Council on 
Geomatics (CCOG) to provide quality geospatial and attributive data (current, accurate, consistent), homogeneous and 
normalized of the entire Canadian road network. The NRN is part of the GeoBase initiative which aims to provide a 
common geospatial infrastructure that is maintained on a regular basis by *closest to source* organizations.

The NRN is distributed in the form of thirteen provincial / territorial datasets consisting of two linear entities 
(road segments and ferry segments), three punctual entities (junctions, blocked passages, and toll points), and three
tabular entities (address ranges, street and place names, and alternative name linkages). Currently, the NRN is 
publicly available on the open government data portal (https://open.canada.ca/en).

The NRN content largely conforms to ISO 14825 (https://www.iso.org/standard/54610.html).

## Setup

The repository of the NRN project is referred to by its actual repository name: `nrn-rrn`.

### Software Dependencies

The `nrn-rrn` has no mandatory software dependencies but highly recommends the software specified in this section. 
Furthermore, documentation for `nrn-rrn` installation and usage will make use of this software since it represents the 
easiest and recommended approach.

#### Anaconda / conda

The `nrn-rrn` is written in pure Python, but has several dependencies written with C libraries. These C libraries can 
be difficult to install (particularly on Windows) and, therefore, it is recommended to create and use the conda virtual 
environment defined in the `nrn-rrn`. conda is an environment and package manager and is the preferable choice for 
dependency management since it provides pre-built binaries for all dependencies of the `nrn-rrn` for all platforms 
(Windows, Mac, Linux).

Anaconda with conda >= 4.9 (the latest version of Anaconda will satisfy this requirement).  
Download: https://docs.anaconda.com/anaconda/install/

Miniconda will also suffice (minimal distribution only containing Python and conda).  
Download: https://docs.conda.io/en/latest/miniconda.html

#### Git

Git is recommended for simpler repository installation and integration of updates.  
Download: https://git-scm.com/downloads

### Installation

Use the following steps to install the `nrn-rrn` repository and conda environment:

1. Install the repository.

   a) Using Git:  
   ```
   git clone https://github.com/jessestewart1/nrn-rrn.git
   ```

   b) Manual install: Download and unzip the repository: https://github.com/jessestewart1/nrn-rrn.


2. Create the conda environment from the `environment.yml` file:
```
conda env create -f <path to environment.yml>
```
