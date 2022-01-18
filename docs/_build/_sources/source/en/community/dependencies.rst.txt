************
Dependencies
************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 2

The NRN project builds upon the capabilities of several open-source Python tools and libraries. Specific dependency
details are outlined in the conda environment file ``environment.yml``. This document briefly explains each of the
dependencies within the NRN dependency ecosystem.

`Click (click) <https://click.palletsprojects.com/>`_
=====================================================

``Click`` is a Python package for creating beautiful command line interfaces in a composable way with as little code as
necessary.

`Fiona (fiona) <https://fiona.readthedocs.io/>`_
================================================

``Fiona`` is ``OGR``'s neat and nimble API for Python programmers. ``Fiona`` reads and writes geographic data files in
standard Python IO style and relies upon familiar Python types and protocols such as files, dictionaries, mappings, and
iterators instead of classes specific to ``OGR``'s implementation.

`GDAL (gdal) <https://gdal.org/>`_
==================================

``GDAL`` is an open source translator library for raster and vector geospatial data formats. The ``GDAL`` library
actually consists of two separate libraries for raster data (``GDAL``) and vector data (``OGR``), collectively referred
to as ``GDAL/OGR``.

`GeoAlchemy 2 (geoalchemy2) <http://geoalchemy-2.readthedocs.org/>`_
====================================================================

``GeoAlchemy 2`` is a support library for ``SQLAlchemy`` that adds support for spatial databases.

`GeoPandas (geopandas) <http://geopandas.readthedocs.io/>`_
===========================================================

``GeoPandas`` extends ``pandas`` data objects to add support for geographic data. ``GeoPandas`` objects can act on
``Shapely`` geometry objects and perform geometric operations.

`Jinja (jinja2) <https://jinja.palletsprojects.com/>`_
======================================================

``Jinja`` is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code
similar to Python syntax. Then the template is passed data to render the final document.

`Matplotlib (matplotlib) <https://matplotlib.org/stable/>`_
===========================================================

``Matplotlib`` is a comprehensive library for creating static, animated, and interactive visualizations in Python.

`MyST-NB (myst-nb) <https://myst-nb.readthedocs.io/>`_
======================================================

``MyST-NB`` is a ``Sphinx`` extension for working with Jupyter Notebook (.ipynb) files.

`NumPy (numpy) <https://numpy.org/>`_
=====================================

``NumPy`` is a library for scientific computing in Python. ``NumPy`` adds support for large, multi-dimensional arrays
and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.

`pandas <https://pandas.pydata.org/>`_
======================================

``pandas`` is a data analysis / manipulation library for Python, providing fast, flexible, and expressive data
structures similar to `R data.frame <https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/data.frame>`_
objects.

`Psycopg (psycopg2) <https://www.psycopg.org/>`_
================================================

``Psycopg`` is a PostgreSQL database adaptor for Python.

`PyData Sphinx Theme (pydata-sphinx-theme) <https://pydata-sphinx-theme.readthedocs.io/>`_
==========================================================================================

``PyData Sphinx Theme`` is a simple, Bootstrap-based Sphinx theme.

`PyGEOS (pygeos) <https://pygeos.readthedocs.io/>`_
===================================================

``PyGEOS`` is a C/Python library with vectorized geometry functions. The geometry operations are done in the geometry
library ``GEOS``. ``PyGEOS`` wraps these operations in ``NumPy`` ufuncs providing a performance improvement when
operating on arrays of geometries.

`Python (python) <https://www.python.org/>`_
============================================

The actual Python installation.

`PyYAML (pyyaml) <https://github.com/yaml/pyyaml>`_
===================================================

``PyYAML`` is a full-featured YAML processing framework for Python.

`Requests (requests) <https://requests.readthedocs.io/>`_
=========================================================

``Requests`` is an elegant and simple HTTP library for Python.

`Shapely (shapely) <https://shapely.readthedocs.io/>`_
======================================================

``Shapely`` is a Python package for manipulation and analysis of planar geometric objects. It is based on the widely
deployed ``GEOS`` (the engine of PostGIS) and ``JTS`` (from which ``GEOS`` is ported) libraries. ``Shapely`` is not
concerned with data formats or coordinate systems, but can be readily integrated with packages that are.

`Sphinx (sphinx) <https://www.sphinx-doc.org/>`_
================================================

``Sphinx`` is a tool that makes it easy to create intelligent and beautiful documentation for Python projects.
``Sphinx`` uses reStructuredText as its markup language.

`SQLAlchemy (sqlalchemy) <https://www.sqlalchemy.org/>`_
========================================================

``SQLAlchemy`` is an SQL toolkit and Object Relational Mapper that gives application developers the full power and
flexibility of SQL in Python.

`python-tabulate (tabulate) <https://pypi.org/project/tabulate/>`_
==================================================================

``python-tabulate`` is a library and command-line utility to pretty-print tabular data in Python.

`tqdm <https://tqdm.github.io/>`_
=================================

``tqdm`` is a fast and extensible progress bar tool for Python.
