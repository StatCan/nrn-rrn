import geopandas as gpd
import logging
import math
import pandas as pd
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

    def __init__(self, dfs: Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]]) -> None:
        """
        Initializes variables for validation functions.

        :param Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]] dfs: dictionary of NRN datasets as (Geo)DataFrames.
        """

        self.errors = defaultdict(list)
        self.id = "uuid"

        # Compile datasets reprojected to a meter-based crs (EPSG:3348).
        self.dfs = {name: df.to_crs("EPSG:3348").copy(deep=True) if "geometry" in df.columns else df.copy(deep=True)
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
                "desc": "Arcs must be >= 3 meters in length.",
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
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            502: {
                "func": self.identifiers_linkages,
                "desc": "Primary - foreign key linkages must be valid.",
                "datasets": ["addrange", "roadseg", "strplaname"]
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

        # TODO

        return errors

    def construction_min_length(self, dataset: str) -> dict:
        """
        Validates: Arcs must be >= 3 meters in length.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def construction_simple(self, dataset: str) -> dict:
        """
        Validates: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

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

        # TODO

        return errors

    def duplication_overlap(self, dataset: str) -> dict:
        """
        Validates: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def encoding_(self, dataset: str) -> dict:
        """
        Validates: Attribute contains one or more question mark (\"?\"), which may be the result of invalid character
            encoding.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

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

        # TODO

        return errors

    def identifiers_linkages(self, dataset: str) -> dict:
        """
        Validates: Primary - foreign key linkages must be valid.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def number_of_lanes_(self, dataset: str) -> dict:
        """
        Validates: Attribute \"nbrlanes\" must be between 1 and 8, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def scope_(self, dataset: str) -> dict:
        """
        Validates: Geometry is not completely within the source region.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

        return errors

    def speed_(self, dataset: str) -> dict:
        """
        Validates: Attribute \"speed\" must be between 5 and 120, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # TODO

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
