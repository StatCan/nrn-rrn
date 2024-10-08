import click
import jinja2
import logging
import re
import sys
import yaml
import zipfile
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from tqdm import tqdm
from tqdm.auto import trange
from typing import Union

filepath = Path(__file__).resolve()
sys.path.insert(1, filepath.parents[1].as_posix())
from utils import helpers
from utils.gui import gui


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Export:
    """Defines an NRN process."""

    def __init__(self, source: str) -> None:
        """
        Initializes an NRN process.

        :param str source: abbreviation for the source province / territory.
        """

        self.source = source.lower()
        self.major_version = None
        self.minor_version = None

        # Configure data paths.
        self.src = filepath.parents[2] / f"data/interim/{self.source}.gpkg"
        self.dst = filepath.parents[2] / f"data/processed/{self.source}"

        # Validate source path.
        if not self.src.exists():
            logger.exception(f"Input data not found: {self.src}.")
            sys.exit(1)

        # Validate destination path.
        if self.dst.exists():
            logger.warning(f"Output namespace already occupied. Removing conflicting contents from: \"{self.dst}\".")
            helpers.delete_contents(self.dst)

        # Configure field defaults and domains.
        self.defaults = {lang: helpers.compile_default_values(lang=lang) for lang in ("en", "fr")}
        self.domains = helpers.compile_domains(mapped_lang="fr")

        # Configure export formats.
        distribution_formats_path = filepath.parent / "distribution_formats"
        formats_en = [f.stem for f in (distribution_formats_path / "en").glob("*")]
        formats_fr = [f.stem for f in (distribution_formats_path / "fr").glob("*")]
        self.distribution_formats = {
            "en": {frmt: helpers.load_yaml(distribution_formats_path / f"en/{frmt}.yaml") for frmt in formats_en},
            "fr": {frmt: helpers.load_yaml(distribution_formats_path / f"fr/{frmt}.yaml") for frmt in formats_fr}
        }

        # Define custom progress bar format.
        # Note: the only change from default is moving the percentage to the right end of the progress bar.
        self.bar_format = "{desc}: |{bar}| {percentage:3.0f}% {r_bar}"

        # Load data.
        self.dframes = helpers.load_gpkg(self.src)

    def __call__(self) -> None:
        """Executes an NRN process."""

        self.configure_release_version()
        self.gen_french_dataframes()
        self.gen_wms_attributes()
        self.export_data()
        self.zip_data()
        self.update_distribution_docs()

    def configure_release_version(self) -> None:
        """Configures the major and minor release versions for the current NRN vintage."""

        logger.info("Configuring NRN release version.")

        # Extract the version number and release year for current source from the release notes.
        release_notes_path = filepath.parent / "distribution_docs/data/release_notes.yaml"
        release_notes = helpers.load_yaml(release_notes_path)

        try:

            # Extract previous release version and date.
            version, release_date = itemgetter("edition", "release_date")(release_notes[self.source])

            # Standardize raw variables.
            self.major_version, self.minor_version = map(int, str(version).split("."))
            release_year = int(str(release_date)[:4])

            # Configure new release version.
            if release_year == datetime.now().year:
                self.minor_version += 1
            else:
                self.major_version += 1
                self.minor_version = 0

        except (IndexError, ValueError) as e:
            logger.exception(f"Unable to extract version number and / or release date from \"{release_notes}\".")
            logger.exception(e)
            sys.exit(1)

        logger.info(f"Configured NRN release version: {self.major_version}.{self.minor_version}")

    def export_data(self) -> None:
        """Exports and packages all data."""

        logger.info("Exporting output data.")

        # Configure export progress bar.
        file_count = 0
        for lang, dfs in self.dframes.items():
            for frmt in self.distribution_formats[lang]:
                file_count += len(set(dfs).intersection(set(self.distribution_formats[lang][frmt]["conform"])))
        export_progress = trange(file_count, desc="Exporting data", bar_format=self.bar_format)

        # Iterate export formats and languages.
        for lang, dfs in self.dframes.items():
            for frmt in self.distribution_formats[lang]:

                # Retrieve export specifications.
                export_specs = self.distribution_formats[lang][frmt]

                # Filter required dataframes.
                dframes = {name: df.copy(deep=True) for name, df in dfs.items() if name in export_specs["conform"]}

                # Configure export directory.
                export_dir, export_file = itemgetter("dir", "file")(export_specs["data"])
                export_dir = self.dst / self.format_path(export_dir) / self.format_path(export_file)

                # Configure formatted layer names.
                for table, specs in export_specs["conform"].items():
                    export_specs["conform"][table]["name"] = self.format_path(specs["name"])

                # Configure export kwargs.
                kwargs = {
                    "driver": export_specs["data"]["driver"],
                    "name_schemas": export_specs["conform"],
                    "keep_uuid": False,
                    "outer_pbar": export_progress
                }

                # Export data.
                helpers.export(dframes, export_dir, **kwargs)

        # Close progress bar.
        export_progress.close()

    def format_path(self, path: Union[Path, str, None]) -> Union[Path, str]:
        """
        Formats a path with class variables: source, major_version, minor_version.

        :param Union[Path, str, None] path: path requiring formatting.
        :return Union[Path, str]: formatted path or empty str.
        """

        if not path:
            return ""

        # Construct replacement dictionary.
        lookup = {k: str(v).upper() for k, v in (("<source>", self.source),
                                                 ("<major_version>", self.major_version),
                                                 ("<minor_version>", self.minor_version))}

        # Replace path keywords with variables.
        path = re.sub(string=str(path),
                      pattern=f"({'|'.join(lookup.keys())})",
                      repl=lambda match: lookup[match.string[match.start(): match.end()]])

        return Path(path)

    def gen_french_dataframes(self) -> None:
        """
        Generate French equivalents of all NRN datasets.
        Note: Only the data values are updated, not the column names.
        """

        logger.info("Generating French dataframes.")

        # Reconfigure dataframes dict to hold English and French data.
        self.dframes = {
            "en": {table: df.copy(deep=True) for table, df in self.dframes.items()},
            "fr": {table: df.copy(deep=True) for table, df in self.dframes.items()}
        }

        # Iterate dataframes and fields.
        for table, df in self.dframes["fr"].items():
            fields = set(df.columns) - {"uuid", "geometry"}
            for field in tqdm(fields, total=len(fields), desc=f"Applying French translations for table: {table}.",
                              bar_format=self.bar_format):

                try:

                    series = df[field].copy(deep=True)

                    # Translate domain values.
                    if field in self.domains[table]:
                        series = helpers.apply_domain(series, self.domains[table][field]["lookup"],
                                                      self.defaults["fr"][table][field])

                    # Translate default values and Nones.
                    series.loc[series == self.defaults["en"][table][field]] = self.defaults["fr"][table][field]
                    if "None" in series:
                        series.loc[series == "None"] = "Aucun"

                    # Store results to dataframe.
                    self.dframes["fr"][table][field] = series.copy(deep=True)

                except (AttributeError, KeyError, ValueError):
                    logger.exception(f"Unable to apply French translations for table: {table}, field: {field}.")
                    sys.exit(1)

    def gen_wms_attributes(self) -> None:
        """Generate WMS attributes for roadseg."""

        logger.info(f"Generating WMS attributes.")

        df = self.dframes["en"]["roadseg"].copy(deep=True)

        # Compile WMS queries.
        data = helpers.load_yaml(filepath.parent / "wms_queries.yaml")["queries"]

        # Iterative WMS scales and queries.
        for attribute in data:
            df[attribute] = 0
            for prov, queries in data[attribute].items():
                if (prov == self.source) and queries:

                    try:

                        # Query type: list or strings
                        if isinstance(queries, list):
                            for query in queries:
                                df.loc[df.query(expr=query).index, attribute] = 1

                        # Query type: all
                        elif queries.lower() == "all":
                            df[attribute] = 1

                        # Query type: string
                        else:
                            df.loc[df.query(expr=queries).index, attribute] = 1

                    except (NameError, SyntaxError) as e:
                        logger.exception(f"Unable to execute query for attribute: {attribute}.")
                        logger.exception(e)
                        sys.exit(1)

        # Replace original dataset.
        self.dframes["en"]["roadseg"] = df.copy(deep=True)

    def update_distribution_docs(self) -> None:
        """
        Writes updated documentation to data/processed for:
            - release notes
        """

        # Update release notes.
        logger.info(f"Updating documentation: release notes.")

        # Compile previous data.
        data = helpers.load_yaml(filepath.parent / "distribution_docs/data/release_notes.yaml")

        # Update release notes - edition, release date, validity date.
        data[self.source]["edition"] = float(f"{self.major_version}.{self.minor_version}")
        data[self.source]["release_date"] = datetime.now().strftime("%Y-%m")
        data[self.source]["validity_date"] = datetime.now().strftime("%Y-%m")

        # Update release notes - number of kilometers.
        # Note: EPSG:3348 used to get geometry lengths in meters.
        kms = int(round(self.dframes["en"]["roadseg"].to_crs("EPSG:3348").length.sum() / 1000, 0))
        data[self.source]["number_of_kilometers"] = f"{kms:,d}"

        # Write updated documents - English and French.
        self.write_documents(data, "en/release_notes", export_yaml=True)
        self.write_documents(data, "fr/release_notes", export_yaml=False)

    def write_documents(self, data: dict, filename: str, export_yaml: bool = True) -> None:
        """
        Updates a document template with a dictionary and exports:
            1) an rst file representing the updated template.
            2) a yaml file containing the updated dictionary.

        :param dict data: dictionary of values used to populate the document template.
        :param str filename: basename of a document in ../distribution_docs to be updated.
        :param bool export_yaml: indicates if the yaml dictionary should be exported, default True.
        """

        # Configure source and destination paths.
        src = filepath.parent / f"distribution_docs/{filename}.rst"
        dst = self.dst / "distribution_docs" / filename

        try:

            # Load document as jinja template.
            with src.open("r") as doc:
                template = jinja2.Template(doc.read())

            # Update template.
            updated_doc = template.render(data)

        except (jinja2.TemplateError, jinja2.TemplateAssertionError, jinja2.UndefinedError) as e:
            logger.exception(f"Unable to render updated Jinja2.Template for: {src}.")
            logger.exception(e)
            sys.exit(1)

        # Export updated document.
        try:

            # Create destination directory structure.
            dst.parent.mkdir(parents=True, exist_ok=True)

            # Write rst.
            with dst.with_suffix(".rst").open("w") as doc:
                doc.write(updated_doc)

            # Write yaml.
            if export_yaml:
                with dst.with_suffix(".yaml").open("w") as doc:
                    yaml.dump(data, doc)

        except (ValueError, yaml.YAMLError) as e:
            logger.exception(f"Unable to write document: {dst}.")
            logger.exception(e)
            sys.exit(1)

    def zip_data(self) -> None:
        """Compresses and zips all export data directories."""

        logger.info("Applying compression and zipping output data directories.")

        # Configure root directory.
        root = filepath.parents[2] / f"data/processed/{self.source}"

        # Configure zip progress bar.
        file_count = 0
        for data_dir in root.glob("*"):
            file_count += len(list(filter(Path.is_file, data_dir.rglob("*"))))
        zip_progress = trange(file_count, desc="Compressing data", bar_format=self.bar_format)

        # Iterate output directories.
        for data_dir in root.glob("*"):

            try:

                # Recursively iterate directory files, compress, and zip contents.
                with zipfile.ZipFile(f"{data_dir}.zip", "w") as zip_f:
                    for file in filter(Path.is_file, data_dir.rglob("*")):

                        zip_progress.set_description_str(f"Compressing file={file.name}")

                        # Configure new relative path inside .zip file.
                        arcname = data_dir.stem / file.relative_to(data_dir)

                        # Write to and compress .zip file.
                        zip_f.write(file, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)
                        zip_progress.update(1)

            except (zipfile.BadZipFile, zipfile.LargeZipFile) as e:
                logger.exception("Unable to compress directory.")
                logger.exception(e)
                sys.exit(1)

            # Remove original directory.
            helpers.delete_contents(data_dir)

        # Close progress bar.
        zip_progress.close()


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
            process = Export(source)
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
