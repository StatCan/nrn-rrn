**********
User Guide
**********

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

General Usage
=============

#TODO: fix this (copied from readme, not formatted yet)

The pipeline is divided into fives stages where each stage is implemented as a directly callable python module,
executed as a command-line interface.

1. Activate the conda virtual environment:

   `conda activate nrn-rrn`

2. For each stage, navigate to the `src/stage_#` directory and use the command line interface `--help` command for
stage-specific options:

   ```
   cd <path to project/src/stage_#>
   python stage.py --help
   ```

Example:

  ```
  C:\Windows\system32>conda activate nrn-rrn

  (nrn-rrn) C:\Windows\system32>cd C:/nrn-rrn/src/stage_1

  (nrn-rrn) C:\nrn-rrn\src\stage_1>python stage.py --help
  Usage: stage.py [OPTIONS] [ab|bc|mb|nb|nl|ns|nt|nu|on|pe|qc|sk|yt]

    Executes an NRN stage.

  Options:
    -r, --remove / --no-remove  Remove pre-existing files within the
                                data/interim directory for the specified source.
                                [default: False]

    --help                      Show this message and exit.

  (nrn-rrn) C:\nrn-rrn\src\stage_1>
  ```

Conform (Source Configuration)
==============================

#TODO: integrate field mapping specifications

Validate (Validations)
======================

#TODO: integrate validation errors doc