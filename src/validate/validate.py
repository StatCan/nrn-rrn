import click
import logging
import sys
from pathlib import Path
from tabulate import tabulate

filepath = Path(__file__).resolve()
sys.path.insert(1, filepath.parents[1].as_posix())
from utils import helpers
from utils.gui import gui
from validation_functions import Validator


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Validate:
    """Defines an NRN process."""

    def __init__(self, source: str) -> None:
        """
        Initializes an NRN process.

        :param str source: abbreviation for the source province / territory.
        """

        self.source = source.lower()
        self.Validator = None

        # Configure data paths.
        self.src = Path(filepath.parents[2] / f"data/interim/{self.source}.gpkg")
        self.dst = filepath.parents[2] / f"data/interim/validations.gpkg"

        # Validate source path.
        if not self.src.exists():
            logger.exception(f"Source not found: \"{self.src}\".")
            sys.exit(1)

        # Validate destination path.
        if self.dst.exists():
            logger.warning(f"Removing conflicting output file: \"{self.dst}\".")
            self.dst.unlink()

        # Load source data.
        self.dframes = helpers.load_gpkg(self.src)

    def __call__(self) -> None:
        """Executes an NRN process."""

        self._validate()
        self._export_errors()

    def _validate(self) -> None:
        """Applies a set of validations to one or more NRN datasets."""

        logger.info("Initiating validator.")

        # Instantiate and execute validator class.
        self.Validator = Validator(self.dframes, source=self.source)
        self.Validator()

    def _export_errors(self) -> None:
        """Exports new subset datasets based on error flags returned by validations."""

        logger.info(f"Exporting subset datasets based on validation errors to: \"{self.dst}\".")

        error_counts = list()

        # Iterate error codes and datasets.
        for code in sorted(self.Validator.errors):

            error_name = self.Validator.validations[code]['func'].__name__
            for dataset, vals in sorted(self.Validator.errors[code].items()):

                # Store error count.
                error_counts.append([f"{code} ({error_name})", dataset, len(vals)])

                # Subset dataset and export to validations output file.
                if len(vals):
                    df_subset = self.dframes[dataset].loc[self.dframes[dataset].index.isin(vals)].copy(deep=True)
                    df_subset.to_file(str(self.dst), driver="GPKG", layer=f"v{code}_{dataset}", index=False)

        # Log validation results summary.
        summary = tabulate(error_counts, headers=["Validation", "Dataset", "Invalid Count"], tablefmt="rst",
                           colalign=("left", "left", "right"))

        logger.info("Validation results:\n" + summary)


@click.command()
@click.argument("source", type=click.Choice(["ab", "bc", "mb", "nb", "nl", "ns", "nt", "nu", "on",
                                             "pe", "qc", "sk", "yt"], case_sensitive=False))
def main(source: str) -> None:
    """
    Executes an NRN process.

    \b
    :param str source: abbreviation for the source province / territory.
    """

    try:

        @helpers.timer
        def run():
            process = Validate(source)
            process()

        run()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":

    # GUI
    if sys.argv[-1] == "--gui":
        main(args=gui(main, calling_script=Path(__file__).resolve()))

    # CLI
    else:
        main()
