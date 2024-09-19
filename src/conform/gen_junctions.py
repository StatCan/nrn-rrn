import geopandas as gpd
import logging
import pandas as pd
import sys
import uuid
from datetime import datetime
from itertools import chain
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely import Point
from typing import Union

filepath = Path(__file__).resolve()
sys.path.insert(1, str(filepath.parents[1]))
from utils import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Junction:
    """Defines the NRN junction generation process."""

    def __init__(self, source: str, target_attributes: dict, roadseg: gpd.GeoDataFrame,
                 ferryseg: Union[gpd.GeoDataFrame, None]) -> None:
        """
        Initializes an NRN stage.

        :param str source: abbreviation for the source province / territory.
        :param dict target_attributes: dictionary definition of NRN junction distribution format.
        :param gpd.GeoDataFrame roadseg: GeoDataFrame of NRN roadseg.
        :param Union[gpd.GeoDataFrame, None] ferryseg: GeoDataFrame of NRN ferryseg.
        """

        self.source = source
        self.target_attributes = target_attributes
        self.roadseg = roadseg.copy(deep=True)
        self.roadseg.index = self.roadseg["uuid"]
        self.ferryseg = None
        if isinstance(ferryseg, gpd.GeoDataFrame):
            self.ferryseg = ferryseg.copy(deep=True)
            self.ferryseg.index = self.ferryseg["uuid"]
        self.junction = None

        # Compile field defaults, dtypes, and domains.
        self.defaults = helpers.compile_default_values(lang="en")["junction"]
        self.dtypes = helpers.compile_dtypes()["junction"]
        self.domains = helpers.compile_domains(mapped_lang="en")["junction"]

        # Load administrative boundary, reprojected to EPSG:4617.
        boundaries = gpd.read_file(filepath.parents[1] / "boundaries.zip", layer="boundaries")
        boundaries = boundaries.loc[boundaries["source"] == self.source].to_crs("EPSG:4617")
        self.boundary = boundaries["geometry"].iloc[0]

    def __call__(self) -> gpd.GeoDataFrame:
        """
        Executes the NRN junction generation methods.

        :return gpd.GeoDataFrame: GeoDataFrame of NRN junction.
        """

        logger.info("Junction generation initiated.")

        self.gen_target_dataframe()
        self.gen_junctions()
        self.gen_attributes()
        self.apply_domains()

        logger.info("Junction generation completed.")

        return self.junction.copy(deep=True)

    def apply_domains(self) -> None:
        """Applies domain restrictions to each column in the target (Geo)DataFrames."""

        logger.info("Applying field domains.")
        field = None

        try:

            for field, domain in self.domains.items():

                logger.info(f"Applying domain to {field}.")

                # Apply domain to series.
                series = self.junction[field].copy(deep=True)
                series = helpers.apply_domain(series, domain["lookup"], self.defaults[field])

                # Force adjust data type.
                series = series.astype(self.dtypes[field])

                # Store results to dataframe.
                self.junction[field] = series.copy(deep=True)

        except (AttributeError, KeyError, ValueError):
            logger.exception(f"Invalid schema definition for table: junction.{field}.")
            sys.exit(1)

    def gen_attributes(self) -> None:
        """Generate the remaining attributes for the output junction dataset."""

        logger.info("Generating remaining dataset attributes.")

        attrs = {"accuracy", "exitnbr"}
        default_exitnbr = self.defaults["exitnbr"]

        # Create attribute lookup dict.
        uuid_attr_lookup = self.roadseg[list(set(self.roadseg.columns).intersection(attrs))].to_dict(orient="dict")
        if isinstance(self.ferryseg, gpd.GeoDataFrame):
            uuid_attr_lookup_ = (self.ferryseg[list(set(self.ferryseg.columns).intersection(attrs))]
                                 .to_dict(orient="dict"))
            for attr in uuid_attr_lookup.keys():
                if attr in uuid_attr_lookup_:
                    uuid_attr_lookup[attr] |= uuid_attr_lookup_[attr]
                else:
                    uuid_attr_lookup[attr] |= dict(zip(self.ferryseg.index, [self.defaults[attr]]*len(self.ferryseg)))

        # Flag records with multiple linked uuids.
        flag = self.junction["uuids"].map(len) > 1

        # Set remaining attributes, where possible.
        self.junction["acqtech"] = "Computed"
        self.junction["metacover"] = "Complete"
        self.junction["credate"] = datetime.today().strftime("%Y%m%d")
        self.junction["datasetnam"] = self.roadseg["datasetnam"].iloc[0]
        self.junction["provider"] = "Federal"
        self.junction["revdate"] = self.defaults["revdate"]
        self.junction["specvers"] = 2

        # Attribute: accuracy. Take maximum value.
        self.junction.loc[flag, "accuracy"] = self.junction.loc[flag, "uuids"].map(
            lambda uuids: max(set(itemgetter(*uuids)(uuid_attr_lookup["accuracy"]))))
        self.junction.loc[~flag, "accuracy"] = self.junction.loc[~flag, "uuids"].map(
            lambda uuids: itemgetter(*uuids)(uuid_attr_lookup["accuracy"]))

        # Attribute: exitnbr. Take first non-default / non-null value, otherwise take the default value.
        self.junction.loc[flag, "exitnbr"] = self.junction.loc[flag, "uuids"].map(
            lambda uuids: [*set(itemgetter(*uuids)(uuid_attr_lookup["exitnbr"])) - {"None", default_exitnbr},
                           default_exitnbr][0])
        self.junction.loc[~flag, "exitnbr"] = self.junction.loc[~flag, "uuids"].map(
            lambda uuids: [*{itemgetter(*uuids)(uuid_attr_lookup["exitnbr"])} - {"None", default_exitnbr},
                           default_exitnbr][0])

        # Delete temporary attribution.
        self.junction.drop(columns=["pt", "uuids"], inplace=True)

    def gen_junctions(self) -> None:
        """Generates a junction GeoDataFrame for all junctypes: Dead End, Ferry, Intersection, and NatProvTer."""

        # Compile and classify junctions.
        logger.info("Compiling and classifying junctions.")

        # Compile all roadseg nodes and group uuids by geometry.
        nodes = self.roadseg["geometry"].map(lambda g: itemgetter(0, -1)(attrgetter("coords")(g))).explode()
        nodes_grouped = pd.DataFrame({"uuid": nodes.index, "pt": nodes.values})\
            .groupby(by="pt", as_index=True)["uuid"].agg(tuple)
        nodes_uuids_lookup = dict(zip(nodes_grouped.index, nodes_grouped.values))

        # Compile all ferryseg nodes and group uuids by geometry.
        ferry_nodes = set()
        if isinstance(self.ferryseg, gpd.GeoDataFrame):
            ferry_nodes = self.ferryseg["geometry"].map(lambda g: itemgetter(0, -1)(attrgetter("coords")(g))).explode()
            ferry_nodes_grouped = pd.DataFrame({"uuid": ferry_nodes.index, "pt": ferry_nodes.values})\
                .groupby(by="pt", as_index=True)["uuid"].agg(tuple)
            ferry_nodes_uuids_lookup = dict(zip(ferry_nodes_grouped.index, ferry_nodes_grouped.values))

            # Update nodes-uuid lookup.
            nodes_uuids_lookup |= ferry_nodes_uuids_lookup

        # Classify junctions.
        ferry = set(ferry_nodes)
        deadend = set(nodes_grouped.loc[nodes_grouped.map(len) == 1].index) - ferry
        intersection = set(nodes_grouped.loc[nodes_grouped.map(len) >= 3].index) - ferry

        # Classify junctions - NatProvTer.
        pts_ = set(chain.from_iterable([deadend, ferry, intersection]))
        pts_df_ = gpd.GeoDataFrame({"pt": list(pts_)}, geometry=list(map(Point, pts_)), crs="EPSG:4617")
        natprovter = pts_ - set(pts_df_.loc[pts_df_.sindex.query(self.boundary, predicate="contains"), "pt"])

        # Remove natprovter junctions from other classifications.
        ferry -= natprovter
        deadend -= natprovter
        intersection -= natprovter

        # Remove ferry-to-ferry-only connections.
        ferry = ferry.intersection(set(nodes))

        # Compile junctions into target dataset.
        logger.info("Compiling junctions into target dataset.")

        # Compile junctions into GeoDataFrame.
        junction_pts = pd.Series(chain.from_iterable([deadend, ferry, intersection, natprovter]))
        junctions = gpd.GeoDataFrame({
            "pt": junction_pts,
            "junctype": None,
            "uuid": [uuid.uuid4().hex for _ in range(len(junction_pts))],
            "uuids": junction_pts.map(nodes_uuids_lookup)
        }, geometry=junction_pts.map(Point), crs="EPSG:4617")

        # Assign junction type.
        for junctype, pts in {"Dead End": deadend, "Ferry": ferry, "Intersection": intersection,
                              "NatProvTer": natprovter}.items():
            junctions.loc[junctions["pt"].isin(pts), "junctype"] = junctype

        # Concatenate data with target DataFrame.
        self.junction = gpd.GeoDataFrame(pd.concat([self.junction, junctions], ignore_index=True, sort=False),
                                         geometry="geometry", crs="EPSG:4617").copy(deep=True)
        self.junction.index = self.junction["uuid"]

    def gen_target_dataframe(self) -> None:
        """Creates empty junction GeoDataFrame."""

        logger.info("Creating target dataframe.")

        self.junction = gpd.GeoDataFrame().assign(**{field: pd.Series(dtype=dtype) for field, dtype in
                                                     self.target_attributes["fields"].items()})
