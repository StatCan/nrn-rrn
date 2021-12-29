import geopandas as gpd
import logging
import math
import pandas as pd
import string
import sys
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from functools import reduce
from itertools import chain, compress, tee
from operator import attrgetter, itemgetter
from pathlib import Path
from scipy.spatial.distance import euclidean
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import split
from typing import Dict, List, Tuple, Union

filepath = Path(__file__).resolve()
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


def ordered_pairs(coords: Tuple[tuple, ...]) -> List[Tuple[tuple, tuple]]:
    """
    Creates an ordered sequence of adjacent coordinate pairs, sorted.
    :param Tuple[tuple, ...] coords: tuple of coordinate tuples.
    :return List[Tuple[tuple, tuple]]: ordered sequence of coordinate pair tuples.
    """

    coords_1, coords_2 = tee(coords)
    next(coords_2, None)

    return sorted(zip(coords_1, coords_2))


class Validator:
    """Handles the execution of validation functions against the NRN datasets."""

    def __init__(self, dfs: Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]], source: str) -> None:
        """
        Initializes variables for validation functions.

        :param str source: abbreviation for the source province / territory.
        :param Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]] dfs: dictionary of NRN datasets as (Geo)DataFrames.
        """

        self.errors = defaultdict(list)
        self.source = source
        self.id = "uuid"
        self.to_crs = "EPSG:3348"
        self.dst = filepath.parents[2] / f"data/interim/{self.source}.gpkg"

        # Compile datasets reprojected to a meter-based crs.
        self.dfs = {name: df.to_crs(self.to_crs).copy(deep=True) if "geometry" in df.columns else df.copy(deep=True)
                    for name, df in dfs.items()}

        # Compile default field values and dtypes.
        self.defaults_all = helpers.compile_default_values()
        self.dtypes_all = helpers.compile_dtypes()

        logger.info("Configuring validations.")

        # Define validation.
        # Note: List validations in order if execution order matters.
        self.validations = {
            101: {
                "func": self.construction_min_length,
                "desc": "Arcs must be >= 3 meters in length, except structures (e.g. Bridges).",
                "datasets": ["ferryseg", "roadseg"]
            },
            102: {
                "func": self.construction_simple,
                "desc": "Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).",
                "datasets": ["ferryseg", "roadseg"]
            },
            103: {
                "func": self.construction_cluster_tolerance,
                "desc": "Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).",
                "datasets": ["ferryseg", "roadseg"]
            },
            201: {
                "func": self.duplication_duplicated,
                "desc": "Features within the same dataset must not be duplicated.",
                "datasets": ["blkpassage", "ferryseg", "roadseg", "tollpoint"]
            },
            202: {
                "func": self.duplication_overlap,
                "desc": "Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).",
                "datasets": ["ferryseg", "roadseg"]
            },
            301: {
                "func": self.connectivity_node_intersection,
                "desc": "Arcs must only connect at endpoints (nodes).",
                "datasets": ["ferryseg", "roadseg"]
            },
            302: {
                "func": self.connectivity_min_distance,
                "desc": "Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).",
                "datasets": ["ferryseg", "roadseg"]
            },
            401: {
                "func": self.dates_length,
                "desc": "Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using "
                        "zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            402: {
                "func": self.dates_combination,
                "desc": "Attributes \"credate\" and \"revdate\" must have a valid yyyymmdd combination.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            403: {
                "func": self.dates_range,
                "desc": "Attributes \"credate\" and \"revdate\" must be between 19600101 and the current date, "
                        "inclusively.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            404: {
                "func": self.dates_order,
                "desc": "Attribute \"credate\" must be <= attribute \"revdate\".",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            501: {
                "func": self.identifiers_32hex,
                "desc": "IDs must be 32 digit hexadecimal strings.",
                "datasets": ["addrange", "altnamlink", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            502: {
                "func": self.identifiers_nid_linkages,
                "desc": "NID linkages must be valid.",
                "datasets": ["addrange", "altnamlink", "blkpassage", "roadseg", "strplaname", "tollpoint"]
            },
            601: {
                "func": self.exit_numbers_nid,
                "desc": "Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all "
                        "arcs sharing an nid.",
                "datasets": ["roadseg"]
            },
            602: {
                "func": self.exit_numbers_roadclass,
                "desc": "When attribute \"exitnbr\" is not equal to the default value or \"None\", attribute "
                        "\"roadclass\" must equal one of the following: \"Expressway / Highway\", \"Freeway\", "
                        "\"Ramp\", \"Rapid Transit\", \"Service Lane\".",
                "datasets": ["roadseg"]
            },
            701: {
                "func": self.ferry_integration_,
                "desc": "Ferry arcs must be connected to a road arc at at least one of their nodes.",
                "datasets": ["ferryseg"]
            },
            801: {
                "func": self.number_of_lanes_,
                "desc": "Attribute \"nbrlanes\" must be between 1 and 8, inclusively.",
                "datasets": ["roadseg"]
            },
            901: {
                "func": self.speed_,
                "desc": "Attribute \"speed\" must be between 5 and 120, inclusively.",
                "datasets": ["roadseg"]
            },
            1001: {
                "func": self.encoding_,
                "desc": "Attribute contains one or more question mark (\"?\"), which may be the result of invalid "
                        "character encoding.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "junction", "roadseg", "strplaname", "tollpoint"]
            },
            1101: {
                "func": self.scope_,
                "desc": "Geometry is not completely within the source region.",
                "datasets": ["blkpassage", "ferryseg", "roadseg", "tollpoint"]
            }
        }

        # Define validation thresholds.
        self._min_len = 3
        self._min_dist = 5
        self._min_cluster_dist = 0.01

        logger.info("Generating reusable geometry attributes.")

        self.pts_id_lookup = {
            "ferryseg": dict(),
            "roadseg": dict()
        }
        self.idx_id_lookup = {
            "ferryseg": dict(),
            "roadseg": dict()
        }

        # Iterate LineString datasets.
        for dataset in ("ferryseg", "roadseg"):
            df = self.dfs[dataset].copy(deep=True)

            # Generate computationally intensive geometry attributes as new columns.
            df["pts_tuple"] = df["geometry"].map(attrgetter("coords")).map(tuple)
            df["pt_start"] = df["pts_tuple"].map(itemgetter(0))
            df["pt_end"] = df["pts_tuple"].map(itemgetter(-1))
            df["pts_ordered_pairs"] = df["pts_tuple"].map(ordered_pairs)

            # Generate computationally intensive lookups.
            pts = df["pts_tuple"].explode()
            pts_df = pd.DataFrame({"pt": pts.values, self.id: pts.index})
            self.pts_id_lookup[dataset] = deepcopy(helpers.groupby_to_list(pts_df, "pt", self.id).map(set).to_dict())
            self.idx_id_lookup[dataset] = deepcopy(dict(zip(range(len(df)), df.index)))

            # Store updated dataframe.
            self.dfs[dataset] = df.copy(deep=True)

    def connectivity_min_distance(self, dataset: str) -> dict:
        """
        Validates: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def connectivity_node_intersection(self, dataset: str) -> dict:
        """
        Validates: Arcs must only connect at endpoints (nodes).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def construction_cluster_tolerance(self, dataset: str) -> dict:
        """
        Validates: Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter arcs to those with > 2 vertices.
        df = df.loc[df["pts_tuple"].map(len) > 2]
        if len(df):

            # Explode coordinate pairs and calculate distances.
            coord_pairs = df["pts_ordered_pairs"].explode()
            coord_dist = coord_pairs.map(lambda pair: euclidean(*pair))

            # Flag pairs with distances that are too small.
            flag = coord_dist < self._min_cluster_dist
            if sum(flag):

                # Export invalid pairs as MultiPoint geometries.
                pts = coord_pairs.loc[flag].map(MultiPoint)
                pts_df = gpd.GeoDataFrame({self.id: pts.index.values}, geometry=[*pts], crs=self.to_crs)

                logger.info(f"Writing to file: {self.dst.name}|layer={dataset}_cluster_tolerance")
                pts_df.to_file(str(self.dst), driver="GPKG", layer=f"{dataset}_cluster_tolerance")

                # Compile error logs.
                vals = set(coord_pairs.loc[flag].index)
                errors["values"] = vals
                errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def construction_min_length(self, dataset: str) -> dict:
        """
        Validates: Arcs must be >= 3 meters in length, except structures (e.g. Bridges).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Flag arcs which are too short.
        flag = df.length < self._min_len
        if sum(flag):

            # Flag isolated structures (structures not connected to another structure).

            # Compile structures.
            structures = df.loc[~df["structure_type"].isin({"Unknown", "None"})]

            # Compile duplicated structure nodes.
            structure_nodes = pd.Series(structures["pt_start"].append(structures["pt_end"]))
            structure_nodes_dups = set(structure_nodes.loc[structure_nodes.duplicated(keep=False)])

            # Flag isolated structures.
            isolated_structure_index = set(structures.loc[~((structures["pt_start"].isin(structure_nodes_dups)) |
                                                            (structures["pt_end"].isin(structure_nodes_dups)))].index)
            isolated_structure_flag = df.index.isin(isolated_structure_index)

            # Modify flag to exclude isolated structures.
            flag = (flag & (~isolated_structure_flag))
            if sum(flag):

                # Compile error logs.
                vals = set(df.loc[flag].index)
                errors["values"] = vals
                errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def construction_simple(self, dataset: str) -> dict:
        """
        Validates: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Flag complex (non-simple) geometries.
        flag = ~df.is_simple
        if sum(flag):

            # Compile error logs.
            vals = set(df.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def dates_combination(self, dataset: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a valid yyyymmdd combination.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Define length-dependant datetime strftime formats.
        strftime = {4: "%Y", 6: "%Y%m", 8: "%Y%m%d"}

        # Iterate date attributes: "credate", "revdate".
        for col in ("credate", "revdate"):

            # Filter to non-default dates.
            default = self.defaults_all[dataset][col]
            series = df.loc[df[col] != default, col].copy(deep=True)

            # Iterate valid lengths.
            for length in (4, 6, 8):
                series_ = series.loc[series.map(lambda val: int(math.log10(val)) + 1) == length].copy(deep=True)

                # Flag records with invalid yyyymmdd combination.
                flag = pd.to_datetime(series_, format=strftime[length], errors="coerce").isna()
                if sum(flag):

                    # Compile error logs.
                    vals = set(series_.loc[flag].index)
                    errors["values"].update(vals)

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def dates_length(self, dataset: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using
            zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Iterate date attributes: "credate", "revdate".
        for col in ("credate", "revdate"):

            # Fetch default value.
            default = self.defaults_all[dataset][col]

            # Flag non-default values which are also not a valid length.
            flag = (df[col] != default) & (~df[col].map(lambda val: int(math.log10(val)) + 1).isin({4, 6, 8}))
            if sum(flag):

                # Compile error logs.
                vals = set(df.loc[flag].index)
                errors["values"].update(vals)
                errors["query"] = f"\"{self.id}\" in {*vals,}"

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def dates_order(self, dataset: str) -> dict:
        """
        Validates: Attribute \"credate\" must be <= attribute \"revdate\".

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        defaults = {"credate": self.defaults_all[dataset]["credate"],
                    "revdate": self.defaults_all[dataset]["revdate"]}
        df_ = df.loc[(df["credate"] != defaults["credate"]) &
                     (df["revdate"] != defaults["revdate"]), ["credate", "revdate"]].copy(deep=True)

        # Flag records with invalid date order.
        flag = df_["credate"] > df_["revdate"]
        if sum(flag):

            # Compile error logs.
            vals = set(df_.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def dates_range(self, dataset: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must be between 19600101 and the current date, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Fetch current date.
        today = int(datetime.today().strftime("%Y%m%d"))

        # Iterate date attributes: "credate", "revdate".
        for col in ("credate", "revdate"):

            # Filter to non-default dates.
            default = self.defaults_all[dataset][col]
            series = df.loc[df[col] != default, col].copy(deep=True)

            # Flag records with invalid date range.
            flag = ~series.between(left=19600101, right=today, inclusive="both")
            if sum(flag):

                # Compile error logs.
                vals = set(series.loc[flag].index)
                errors["values"].update(vals)

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def duplication_duplicated(self, dataset: str) -> dict:
        """
        Validates: Features within the same dataset must not be duplicated.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter arcs to those with duplicated lengths.
        df = df.loc[df.length.duplicated(keep=False)]
        if len(df):

            # Filter arcs to those with duplicated nodes.
            df = df.loc[df[["pt_start", "pt_end"]].agg(set, axis=1).map(tuple).duplicated(keep=False)]

            # Flag duplicated geometries.
            dups = df.loc[df["geometry"].map(lambda g1: df["geometry"].map(lambda g2: g1.equals(g2)).sum() > 1)]
            if len(dups):

                # Compile error logs.
                vals = set(dups.index)
                errors["values"] = vals
                errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def duplication_overlap(self, dataset: str) -> dict:
        """
        Validates: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Query arcs which overlap each segment.
        overlaps = df["geometry"].map(lambda g: set(df.sindex.query(g, predicate="overlaps")))

        # Flag arcs which have one or more overlapping segments.
        flag = overlaps.map(len) > 0
        if sum(flag):

            # Compile error logs.
            vals = set(overlaps.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def encoding_(self, dataset: str) -> dict:
        """
        Validates: Attribute contains one or more question mark (\"?\"), which may be the result of invalid character
            encoding.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Iterate string columns.
        for col in set(df.select_dtypes(include="object").columns) - {"geometry", "nid", "uuid"}:

            # Flag records containing one or more question mark ("?").
            flag = df[col].str.contains("?", regex=False)

            # Compile error logs.
            vals = set(df.loc[flag].index)
            errors["values"].update(vals)

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def exit_numbers_nid(self, dataset: str) -> dict:
        """
        Validates: Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all arcs
            sharing an nid.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def exit_numbers_roadclass(self, dataset: str) -> dict:
        """
        Validates: When attribute \"exitnbr\" is not equal to the default value or \"None\", attribute \"roadclass\"
            must equal one of the following: \"Expressway / Highway\", \"Freeway\", \"Ramp\", \"Rapid Transit\",
            \"Service Lane\".

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def ferry_integration_(self, dataset: str) -> dict:
        """
        Validates: Ferry arcs must be connected to a road arc at at least one of their nodes.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def identifiers_32hex(self, dataset: str) -> dict:
        """
        Validates: IDs must be 32 digit hexadecimal strings.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Compile hexadecimal characters.
        hexdigits = set(string.hexdigits)

        # Configure identifier columns.
        identifiers = {
            "addrange": ["l_altnanid", "l_offnanid", "nid", "r_altnanid", "r_offnanid"],
            "altnamlink": ["nid", "strnamenid"],
            "blkpassage": ["nid", "roadnid"],
            "ferryseg": ["nid"],
            "roadseg": ["adrangenid", "nid"],
            "strplaname": ["nid"],
            "tollpoint": ["nid", "roadnid"]
        }

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Iterate identifiers.
        for col in identifiers[dataset]:

            # Filter to non-default and non-None values, except for nids.
            if col == "nid":
                series = df[col].copy(deep=True)
            else:
                default = self.defaults_all[dataset][col]
                series = df.loc[(df[col] != default) & (df[col] != "None")].copy(deep=True)

            # Flag records with non-hexadecimal or non-32 digit identifiers.
            flag = (series.astype(str).map(len) != 32) | (series.map(lambda val: not set(val).issubset(hexdigits)))
            if sum(flag):

                # Compile error logs.
                vals = set(series.loc[flag].index)
                errors["values"].update(vals)

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def identifiers_nid_linkages(self, dataset: str) -> dict:
        """
        Validates: NID linkages must be valid.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Configure dataset nid linkages.
        linkages = {
            "addrange":
                {
                    "roadseg": ["adrangenid"]
                },
            "altnamlink":
                {
                    "addrange": ["l_altnanid", "r_altnanid"]
                },
            "roadseg":
                {
                    "blkpassage": ["roadnid"],
                    "tollpoint": ["roadnid"]
                },
            "strplaname":
                {
                    "addrange": ["l_offnanid", "r_offnanid"],
                    "altnamlink": ["strnamenid"]
                }
        }

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Iterate datasets whose nids the current dataset links to.
        for nid_dataset in filter(lambda name: dataset in linkages[name],
                                  set(linkages[dataset]).intersection(self.dfs)):

            # Compile linked nids.
            nids = set(self.dfs[nid_dataset]["nid"])

            # Iterate columns which link to the nid dataset.
            for col in linkages[nid_dataset][dataset]:

                # Flag missing, non-None identifiers.
                invalid_ids = set(df[col]) - nids - {"None"}
                if len(invalid_ids):

                    # Compile error logs.
                    vals = set(df.loc[df[col].isin(invalid_ids)].index)
                    errors["values"] = vals

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}"

        return errors

    def number_of_lanes_(self, dataset: str) -> dict:
        """
        Validates: Attribute \"nbrlanes\" must be between 1 and 8, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset]["nbrlanes"]
        series = df.loc[df["nbrlanes"] != default, "nbrlanes"].copy(deep=True)

        # Flag records with invalid values.
        flag = ~series.between(left=1, right=8, inclusive="both")
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def scope_(self, dataset: str) -> dict:
        """
        Validates: Geometry is not completely within the source region.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Load administrative boundary, reprojected to meter-based crs.
        boundaries = gpd.read_file(filepath.parent / "boundaries.zip", layer="boundaries")
        boundaries = boundaries.loc[boundaries["source"] == self.source].to_crs(self.to_crs)
        boundary = boundaries["geometry"].iloc[0]

        # Compile indexes of geometries not completely within the source region.
        invalid_idxs = list(set(range(len(df))) - set(df.sindex.query(boundary, predicate="contains")))
        if len(invalid_idxs):

            # Compile error logs.
            vals = set(df.iloc[invalid_idxs].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def speed_(self, dataset: str) -> dict:
        """
        Validates: Attribute \"speed\" must be between 5 and 120, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset]["speed"]
        series = df.loc[df["speed"] != default, "speed"].copy(deep=True)

        # Flag records with invalid values.
        flag = ~series.between(left=5, right=120, inclusive="both")
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}"

        return errors

    def execute(self) -> None:
        """Orchestrates the execution of validation functions and compiles the resulting errors."""

        try:

            # Iterate validations.
            for code, params in self.validations.items():
                func, description, datasets = itemgetter("func", "desc", "datasets")(params)

                # Iterate datasets.
                for dataset in datasets:

                    logger.info(f"Applying validation E{code}: \"{func.__name__}\"; dataset={dataset}.")

                    # Execute validation and store non-empty results.
                    results = func(dataset)
                    if len(results["values"]):
                        self.errors[f"E{code} - {dataset} - {description}"] = deepcopy(results)

        except (KeyError, SyntaxError, ValueError) as e:
            logger.exception("Unable to apply validation.")
            logger.exception(e)
            sys.exit(1)
