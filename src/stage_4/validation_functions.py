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
from typing import List, Tuple, Union

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
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            102: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            103: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            201: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            202: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            301: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            302: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            401: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            402: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            403: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            404: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            405: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            406: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            501: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            502: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            601: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            701: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            801: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            901: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            1001: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            1101: {
                "func": self._,
                "desc": "_",
                "datasets": []
            },
            1201: {
                "func": self._,
                "desc": "_",
                "datasets": []
            }
        }

        # Define validation thresholds.
        self._min_len = 3
        self._min_dist = 5
        self._min_cluster_dist = 0.01

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