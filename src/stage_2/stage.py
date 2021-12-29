import click
import geopandas as gpd
import logging
import pandas as pd
import sys
import uuid
from datetime import datetime
from itertools import chain
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely.geometry import Point

filepath = Path(__file__).resolve()
sys.path.insert(1, str(filepath.parents[1]))
import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Stage:
    """Defines an NRN stage."""

    def __init__(self, source: str) -> None:
        """
        Initializes an NRN stage.

        :param str source: abbreviation for the source province / territory.
        """

        self.stage = 2
        self.source = source.lower()
        self.boundary = None

        # Configure and validate input data path.
        self.data_path = filepath.parents[2] / f"data/interim/{self.source}.gpkg"
        if not self.data_path.exists():
            logger.exception(f"Input data not found: \"{self.data_path}\".")
            sys.exit(1)

        # Compile field defaults, dtypes, and domains.
        self.defaults = helpers.compile_default_values(lang="en")["junction"]
        self.dtypes = helpers.compile_dtypes()["junction"]
        self.domains = helpers.compile_domains(mapped_lang="en")["junction"]

        # Load data.
        self.dframes = helpers.load_gpkg(self.data_path, layers=["ferryseg", "roadseg"])

        # Load administrative boundary, reprojected to EPSG:4617.
        boundaries = gpd.read_file(filepath.parent / "boundaries.zip", layer="boundaries")
        boundaries = boundaries.loc[boundaries["source"] == self.source].to_crs("EPSG:4617")
        self.boundary = boundaries["geometry"].iloc[0]

    def apply_domains(self) -> None:
        """Applies domain restrictions to each column in the target (Geo)DataFrames."""

        logger.info("Applying field domains.")
        field = None

        try:

            for field, domain in self.domains.items():

                logger.info(f"Applying domain to field: {field}.")

                # Apply domain to series.
                series = self.dframes["junction"][field].copy(deep=True)
                series = helpers.apply_domain(series, domain["lookup"], self.defaults[field])

                # Force adjust data type.
                series = series.astype(self.dtypes[field])

                # Store results to dataframe.
                self.dframes["junction"][field] = series.copy(deep=True)

        except (AttributeError, KeyError, ValueError):
            logger.exception(f"Invalid schema definition for table: junction, field: {field}.")
            sys.exit(1)

    def compile_target_attributes(self) -> None:
        """Compiles the yaml file for the target (Geo)DataFrames (distribution format) into a dictionary."""

        logger.info("Compiling target attributes yaml.")
        table = field = None

        # Load yaml.
        self.target_attributes = helpers.load_yaml(filepath.parents[1] / "distribution_format.yaml")

        # Remove field length from dtype attribute.
        logger.info("Configuring target attributes.")
        try:

            for table in self.target_attributes:
                for field, vals in self.target_attributes[table]["fields"].items():
                    self.target_attributes[table]["fields"][field] = vals[0]

        except (AttributeError, KeyError, ValueError):
            logger.exception(f"Invalid schema definition for table: {table}, field: {field}.")
            sys.exit(1)

    def gen_attributes(self) -> None:
        """Generate the remaining attributes for the output junction dataset."""

        logger.info("Generating remaining dataset attributes.")

        # Create attribute lookup dict.
        uuid_attr_lookup = self.dframes["roadseg"][list(set(self.dframes["roadseg"].columns) - {"geometry"})]\
            .to_dict(orient="dict")

        # Flag records with multiple linked uuids.
        flag = self.dframes["junction"]["uuids"].map(len) > 1

        # Set remaining attributes, where possible.
        self.dframes["junction"]["acqtech"] = "Computed"
        self.dframes["junction"]["metacover"] = "Complete"
        self.dframes["junction"]["credate"] = datetime.today().strftime("%Y%m%d")
        self.dframes["junction"]["datasetnam"] = self.dframes["roadseg"]["datasetnam"].iloc[0]
        self.dframes["junction"]["provider"] = "Federal"
        self.dframes["junction"]["revdate"] = self.defaults["revdate"]

        # Attribute: accuracy. Take maximum value.
        self.dframes["junction"].loc[flag, "accuracy"] = self.dframes["junction"].loc[flag, "uuids"].map(
            lambda uuids: max(set(itemgetter(*uuids)(uuid_attr_lookup["accuracy"]))))
        self.dframes["junction"].loc[~flag, "accuracy"] = self.dframes["junction"].loc[~flag, "uuids"].map(
            lambda uuids: itemgetter(*uuids)(uuid_attr_lookup["accuracy"]))

        # Attribute: exitnbr. Take first non-default / non-null value, otherwise take the default value.
        default_exitnbr = self.defaults["exitnbr"]
        self.dframes["junction"].loc[flag, "exitnbr"] = self.dframes["junction"].loc[flag, "uuids"].map(
            lambda uuids: [*set(itemgetter(*uuids)(uuid_attr_lookup["exitnbr"])) - {"None", default_exitnbr},
                           default_exitnbr][0])
        self.dframes["junction"].loc[~flag, "exitnbr"] = self.dframes["junction"].loc[~flag, "uuids"].map(
            lambda uuids: [*{itemgetter(*uuids)(uuid_attr_lookup["exitnbr"])} - {"None", default_exitnbr},
                           default_exitnbr][0])

        # Delete temporary attribution.
        self.dframes["junction"].drop(columns=["pt", "uuids"], inplace=True)

    def gen_junctions(self) -> None:
        """Generates a junction GeoDataFrame for all junctypes: Dead End, Ferry, Intersection, and NatProvTer."""

        logger.info("Generating junctions.")
        roadseg = self.dframes["roadseg"].copy(deep=True)

        # Compile and classify junctions.
        logger.info("Compiling and classifying junctions.")

        # Compile all nodes and group uuids by geometry.
        nodes = roadseg["geometry"].map(lambda g: itemgetter(0, -1)(attrgetter("coords")(g))).explode()
        nodes_df = pd.DataFrame({"uuid": nodes.index, "pt": nodes.values})
        nodes_grouped = helpers.groupby_to_list(nodes_df, group_field="pt", list_field="uuid")
        nodes_grouped_df = gpd.GeoDataFrame({"pt": nodes_grouped.index, "uuids": nodes_grouped.values},
                                            geometry=nodes_grouped.index.map(Point).values, crs="EPSG:4617")

        # Classify junctions.
        ferry = set(self.dframes["ferryseg"]["geometry"].map(
            lambda g: itemgetter(0, -1)(attrgetter("coords")(g))).explode())
        deadend = set(nodes_grouped_df.loc[(nodes_grouped_df["uuids"].map(len) == 1) &
                                           (~nodes_grouped_df["pt"].isin(ferry)), "pt"])
        intersection = set(nodes_grouped_df.loc[(nodes_grouped_df["uuids"].map(len) >= 3) &
                                                (~nodes_grouped_df["pt"].isin(ferry)), "pt"])
        natprovter = set(chain.from_iterable([deadend, ferry, intersection])) -\
                     set(nodes_grouped_df.loc[nodes_grouped_df.sindex.query(self.boundary, predicate="contains"), "pt"])

        # Remove natprovter junctions from other classifications.
        ferry = ferry - natprovter
        deadend = deadend - natprovter
        intersection = intersection - natprovter

        # Compile junctions into target dataset.
        logger.info("Compiling junctions into target dataset.")

        # Compile junctions into GeoDataFrame.
        junction_pts = set(chain.from_iterable([deadend, ferry, intersection]))
        junctions = nodes_grouped_df.loc[nodes_grouped_df["pt"].isin(junction_pts)].copy(deep=True)
        junctions["junctype"] = None
        junctions["uuid"] = [uuid.uuid4().hex for _ in range(len(junctions))]
        for junctype, pts in {"Dead End": deadend, "Ferry": ferry, "Intersection": intersection,
                              "NatProvTer": natprovter}.items():
            junctions.loc[junctions["pt"].isin(pts), "junctype"] = junctype

        # Concatenate data with target DataFrame.
        self.dframes["junction"] = gpd.GeoDataFrame(
            pd.concat([self.junction, junctions], ignore_index=True, sort=False), crs="EPSG:4617").copy(deep=True)
        self.dframes["junction"].index = self.dframes["junction"]["uuid"]

    def gen_target_dataframe(self) -> None:
        """Creates empty junction GeoDataFrame."""

        logger.info("Creating target dataframe.")

        self.junction = gpd.GeoDataFrame().assign(**{field: pd.Series(dtype=dtype) for field, dtype in
                                                     self.target_attributes["junction"]["fields"].items()})

    def execute(self) -> None:
        """Executes an NRN stage."""

        self.compile_target_attributes()
        self.gen_target_dataframe()
        self.gen_junctions()
        self.gen_attributes()
        self.apply_domains()
        helpers.export({"junction": self.dframes["junction"]}, self.data_path)


@click.command()
@click.argument("source", type=click.Choice("ab bc mb nb nl ns nt nu on pe qc sk yt".split(), False))
def main(source: str) -> None:
    """
    Executes an NRN stage.

    :param str source: abbreviation for the source province / territory.
    """

    try:

        with helpers.Timer():
            stage = Stage(source)
            stage.execute()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
