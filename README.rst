National Road Network (NRN)
===========================

.. image:: https://img.shields.io/badge/Repository-nrn--rrn-brightgreen.svg?style=flat-square&logo=github
   :target: https://github.com/StatCan/nrn-rrn
.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square
   :target: https://opensource.org/licenses/BSD-3-Clause
.. image:: https://readthedocs.org/projects/nrn-rrn-docs/badge/?style=flat-square
   :target: https://nrn-rrn-docs.readthedocs.io/en/latest/

Description
-----------

The NRN was adopted by members from the Inter-Agency Committee on Geomatics (IACG) and the Canadian Council on 
Geomatics (CCOG) to provide quality geospatial and attributive data (current, accurate, consistent), homogeneous and 
normalized of the entire Canadian road network. The NRN is part of the GeoBase initiative which aims to provide a 
common geospatial infrastructure that is maintained on a regular basis by *closest to source* organizations.

The NRN is distributed in the form of thirteen provincial / territorial datasets consisting of two linear entities 
(road segments and ferry segments), three punctual entities (junctions, blocked passages, and toll points), and three
tabular entities (address ranges, street and place names, and alternative name linkages). Currently, the NRN is
publicly available on the `Open Government data portal <https://open.canada.ca/en>`_.

The NRN content largely conforms to `ISO 14825 <https://www.iso.org/standard/54610.html>`_.

Setup
-----

The repository of the NRN project is referred to by its actual repository name: ``nrn-rrn``.

Software Dependencies
^^^^^^^^^^^^^^^^^^^^^

The ``nrn-rrn`` has no mandatory software dependencies but highly recommends the software specified in this section.
Furthermore, documentation for ``nrn-rrn`` installation and usage will make use of this software since it represents
the easiest and recommended approach.

Anaconda / conda
""""""""""""""""

The ``nrn-rrn`` is written in pure Python, but has several dependencies written with C libraries. These C libraries can
be difficult to install (particularly on Windows) and, therefore, it is recommended to create and use the conda virtual 
environment defined in the ``nrn-rrn``. conda is an environment and package manager and is the preferable choice for
dependency management since it provides pre-built binaries for all dependencies of the ``nrn-rrn`` for all platforms
(Windows, Mac, Linux).

| `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ with conda >= 4.9.
| `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ will also suffice (minimal distribution only containing
  Python and conda).

Git
"""

| `Git <https://git-scm.com/downloads>`_ is recommended for simpler repository installation and integration of updates.

Installation
^^^^^^^^^^^^

Use the following steps to install the ``nrn-rrn`` repository and conda environment:

1. Install the repository.

  a) Using Git::

      git clone https://github.com/StatCan/nrn-rrn.git

  b) Manual install: Download and unzip the `repository <https://github.com/StatCan/nrn-rrn>`_.

2. Create the conda environment from the ``environment.yml`` file::

    conda env create -f nrn-rrn/environment.yml
