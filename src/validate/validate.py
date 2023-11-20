import click
import logging
import sys
from itertools import chain
from pathlib import Path

filepath = Path(__file__).resolve()
sys.path.insert(1, str(filepath.parents[1]))
import helpers
from validation_functions import Validator


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)

# Create logger for validation errors.
logger_validations = logging.getLogger("validations")
logger_validations.setLevel(logging.WARNING)


class Validate:
    """Defines an NRN process."""

    def __init__(self, source: str, remove: bool = False) -> None:
        """
        Initializes an NRN process.

        :param str source: abbreviation for the source province / territory.
        :param bool remove: remove pre-existing output file (validations.log), default False.
        """

        self.source = source.lower()
        self.remove = remove
        self.Validator = None

        # Configure data paths.
        self.src = Path(filepath.parents[2] / f"data/interim/{self.source}.gpkg")
        self.validations_log = Path(self.src.parent / "validations.log")

        # Validate source path.
        if not self.src.exists():
            logger.exception(f"Source not found: \"{self.src}\".")
            sys.exit(1)

        # Validate destination path.
        if self.validations_log.exists():
            if remove:
                logger.info(f"Removing conflicting file: \"{self.validations_log}\".")
                self.validations_log.unlink()
            else:
                logger.exception(f"Conflicting file exists (\"{self.validations_log}\") but remove=False. Set "
                                 f"remove=True (-r) or manually clear the output namespace.")
                sys.exit(1)

        # Load source data.
        self.dframes = helpers.load_gpkg(self.src)

    def __call__(self) -> None:
        """Executes an NRN process."""

        self._validate()
        self.log_errors()

    def _validate(self) -> None:
        """Applies a set of validations to one or more NRN datasets."""

        logger.info("Initiating validator.")

        # Instantiate and execute validator class.
        self.Validator = Validator(self.dframes, source=self.source)
        self.Validator()

    def log_errors(self) -> None:
        """Outputs error logs returned by validation functions."""

        logger.info(f"Writing error logs: \"{self.validations_log}\".")

        # Quantify errors.
        identifiers = list(chain.from_iterable(self.Validator.errors.values()))
        total_records = len(identifiers)
        total_unique_records = len(set(identifiers))

        # Add File Handler to validation logger.
        f_handler = logging.FileHandler(self.validations_log)
        f_handler.setLevel(logging.WARNING)
        f_handler.setFormatter(logger.handlers[0].formatter)
        logger_validations.addHandler(f_handler)

        # Iterate and log errors.
        for code, vals in sorted(self.Validator.errors.items()):
            if len(vals):

                # Format and write logs.
                values = "\n".join(map(str, vals))
                logger_validations.warning(f"{code}\n\nValues:\n{values}\n")

        logger.info(f"Total records flagged by validations: {total_records:,d}.")
        logger.info(f"Total unique records flagged by validations: {total_unique_records:,d}.")


@click.command()
@click.argument("source", type=click.Choice("ab bc mb nb nl ns nt nu on pe qc sk yt".split(), False))
@click.option("--remove / --no-remove", "-r", default=False, show_default=True,
              help="Remove pre-existing output file (validations.log).")
def main(source: str, remove: bool = False) -> None:
    """
    Executes an NRN process.

    \b
    :param str source: abbreviation for the source province / territory.
    :param bool remove: remove pre-existing output file (validations.log), default False.
    """

    try:

        with helpers.Timer():
            process = Validate(source, remove)
            process()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
