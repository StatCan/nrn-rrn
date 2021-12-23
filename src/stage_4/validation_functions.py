import geopandas as gpd
import logging
import pandas as pd
import sys
from collections import defaultdict
from copy import deepcopy
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
                "datasets": []
            },
            102: {
                "func": self.construction_simple,
                "desc": "Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).",
                "datasets": []
            },
            103: {
                "func": self.construction_cluster_tolerance,
                "desc": "Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).",
                "datasets": []
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
                "func": self.dates_year,
                "desc": "Attributes \"credate\" and \"revdate\" must have a year (first 4 digits) between 1960 and the "
                        "current year, inclusively.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            403: {
                "func": self.dates_month,
                "desc": "Attributes \"credate\" and \"revdate\" must have a month (digits 5 and 6) between 01 and 12, "
                        "inclusively.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            404: {
                "func": self.dates_day,
                "desc": "Attributes \"credate\" and \"revdate\" must have a day (digits 7 and 8) between 01 and the "
                        "monthly maximum, inclusively.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            405: {
                "func": self.dates_future,
                "desc": "Attributes \"credate\" and \"revdate\" must be <= today.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"]
            },
            406: {
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

    def connectivity_min_distance(self) -> dict:
        """
        Validates: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def connectivity_node_intersection(self) -> dict:
        """
        Validates: Arcs must only connect at endpoints (nodes).

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def construction_cluster_tolerance(self) -> dict:
        """
        Validates: Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def construction_min_length(self) -> dict:
        """
        Validates: Arcs must be >= 3 meters in length.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def construction_simple(self) -> dict:
        """
        Validates: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_day(self) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a day (digits 7 and 8) between 01 and the monthly
            maximum, inclusively.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_future(self) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must be <= today.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_length(self) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using
            zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_month(self) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a month (digits 5 and 6) between 01 and 12,
            inclusively.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_order(self) -> dict:
        """
        Validates: Attribute \"credate\" must be <= attribute \"revdate\".

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def dates_year(self) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a year (first 4 digits) between 1960 and the
            current year, inclusively.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def duplication_duplicated(self) -> dict:
        """
        Validates: Features within the same dataset must not be duplicated.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def duplication_overlap(self) -> dict:
        """
        Validates: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def encoding_(self) -> dict:
        """
        Validates: Attribute contains one or more question mark (\"?\"), which may be the result of invalid character
            encoding.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def exit_numbers_nid(self) -> dict:
        """
        Validates: Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all arcs
            sharing an nid.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def exit_numbers_roadclass(self) -> dict:
        """
        Validates: When attribute \"exitnbr\" is not equal to the default value or \"None\", attribute \"roadclass\"
            must equal one of the following: \"Expressway / Highway\", \"Freeway\", \"Ramp\", \"Rapid Transit\",
            \"Service Lane\".

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def ferry_integration_(self) -> dict:
        """
        Validates: Ferry arcs must be connected to a road arc at at least one of their nodes.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def identifiers_32hex(self) -> dict:
        """
        Validates: IDs must be 32 digit hexadecimal strings.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def identifiers_linkages(self) -> dict:
        """
        Validates: Primary - foreign key linkages must be valid.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def number_of_lanes_(self) -> dict:
        """
        Validates: Attribute \"nbrlanes\" must be between 1 and 8, inclusively.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def scope_(self) -> dict:
        """
        Validates: Geometry is not completely within the source region.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def speed_(self) -> dict:
        """
        Validates: Attribute \"speed\" must be between 5 and 120, inclusively.

        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": list(), "query": None}

        # TODO

        return errors

    def execute(self) -> None:
        """Orchestrates the execution of validation functions and compiles the resulting errors."""

        try:

            # Iterate validations.
            for code, params in self.validations.items():
                func, description = itemgetter("func", "desc")(params)

                logger.info(f"Applying validation E{code}: \"{func.__name__}\".")

                # Execute validation and store non-empty results.
                results = func()
                if len(results["values"]):
                    self.errors[f"E{code} - {description}"] = deepcopy(results)

        except (KeyError, SyntaxError, ValueError) as e:
            logger.exception("Unable to apply validation.")
            logger.exception(e)
            sys.exit(1)