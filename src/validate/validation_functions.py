import geopandas as gpd
import logging
import math
import pandas as pd
import string
import sys
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from itertools import chain, compress, tee
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely.geometry import MultiPoint, Point
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
    :return List[Tuple[tuple, tuple], ...]: ordered sequence of coordinate pair tuples.
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

        # Compile default field values.
        self.defaults_all = helpers.compile_default_values()

        # Load administrative boundary, reprojected to meter-based crs.
        boundaries = gpd.read_file(filepath.parents[1] / "boundaries.zip", layer="boundaries")
        boundaries = boundaries.loc[boundaries["source"] == self.source].to_crs(self.to_crs)
        self.boundary = boundaries["geometry"].iloc[0]

        logger.info("Configuring validations.")

        # Define validation.
        # Note: List validations in order if execution order matters.
        self.validations = {
            101: {
                "func": self.construction_min_length,
                "desc": "Arcs must be >= 3 meters in length, except structures (e.g. Bridges).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            102: {
                "func": self.construction_simple,
                "desc": "Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            103: {
                "func": self.construction_cluster_tolerance,
                "desc": "Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            201: {
                "func": self.duplication_duplicated,
                "desc": "Features within the same dataset must not be duplicated.",
                "datasets": ["blkpassage", "ferryseg", "roadseg", "tollpoint"],
                "iter_cols": None
            },
            202: {
                "func": self.duplication_overlap,
                "desc": "Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            301: {
                "func": self.connectivity_node_intersection,
                "desc": "Arcs must only connect at endpoints (nodes).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            302: {
                "func": self.connectivity_min_distance,
                "desc": "Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).",
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            401: {
                "func": self.dates_length,
                "desc": "Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using "
                        "zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            402: {
                "func": self.dates_combination,
                "desc": "Attributes \"credate\" and \"revdate\" must have a valid YYYYMMDD combination.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            403: {
                "func": self.dates_range,
                "desc": "Attributes \"credate\" and \"revdate\" must be between 19600101 and the current date, "
                        "inclusively.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            501: {
                "func": self.identifiers_32hex,
                "desc": "IDs must be 32 digit hexadecimal strings.",
                "datasets": ["addrange", "altnamlink", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": {
                    "addrange": ["l_altnanid", "l_offnanid", "nid", "r_altnanid", "r_offnanid"],
                    "altnamlink": ["nid", "strnamenid"],
                    "blkpassage": ["nid", "roadnid"],
                    "ferryseg": ["nid"],
                    "roadseg": ["adrangenid", "nid"],
                    "strplaname": ["nid"],
                    "tollpoint": ["nid", "roadnid"]
                }
            },
            502: {
                "func": self.identifiers_nid_linkages,
                "desc": "NID linkages must be valid.",
                "datasets": ["addrange", "altnamlink", "blkpassage", "roadseg", "tollpoint"],
                "iter_cols": {
                    "addrange": ["l_altnanid", "l_offnanid", "r_altnanid", "r_offnanid"],
                    "altnamlink": ["strnamenid"],
                    "blkpassage": ["roadnid"],
                    "roadseg": ["adrangenid"],
                    "tollpoint": ["roadnid"]
                }
            },
            601: {
                "func": self.exit_numbers_nid,
                "desc": "Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all "
                        "arcs sharing an NID.",
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            602: {
                "func": self.exit_numbers_roadclass,
                "desc": "When attribute \"exitnbr\" is not equal to the default value or \"None\", attribute "
                        "\"roadclass\" must equal one of the following: \"Expressway / Highway\", \"Freeway\", "
                        "\"Ramp\", \"Rapid Transit\", \"Service Lane\".",
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            701: {
                "func": self.ferry_integration_,
                "desc": "Ferry arcs must be connected to a road arc at at least one of their nodes.",
                "datasets": ["ferryseg"],
                "iter_cols": None
            },
            801: {
                "func": self.number_of_lanes_,
                "desc": "Attribute \"nbrlanes\" must be between 1 and 8, inclusively.",
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            901: {
                "func": self.speed_,
                "desc": "Attribute \"speed\" must be between 5 and 120, inclusively.",
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            1001: {
                "func": self.encoding_,
                "desc": "Attribute contains one or more question mark (\"?\"), which may be the result of invalid "
                        "character encoding.",
                "datasets": ["addrange", "blkpassage", "ferryseg", "junction", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": {name: set(df.select_dtypes(include="object").columns) - {"geometry", "nid", "uuid"} for
                              name, df in self.dfs.items()}
            },
            1101: {
                "func": self.scope_,
                "desc": "Geometry is not completely within the source region.",
                "datasets": ["blkpassage", "ferryseg", "roadseg", "tollpoint"],
                "iter_cols": None
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

    def __call__(self) -> None:
        """Orchestrates the execution of validation functions and compiles the resulting errors."""

        try:

            # Iterate validations.
            for code, params in self.validations.items():
                func, desc, datasets, iter_cols = itemgetter("func", "desc", "datasets", "iter_cols")(params)

                # Reconfigure iter_cols as dict.
                if isinstance(iter_cols, list):
                    iter_cols = {dataset: iter_cols for dataset in datasets}

                # Iterate datasets, if they exist.
                for dataset in set(datasets).intersection(self.dfs):

                    # Iterate columns, if required.
                    if iter_cols:
                        for col in iter_cols[dataset]:

                            logger.info(f"Applying validation E{code}: \"{func.__name__}\"; target={dataset}.{col}.")

                            # Execute validation and store non-empty results.
                            results = func(dataset, col=col)
                            if len(results["values"]):
                                self.errors[f"E{code} - {dataset}.{col} - {desc}"] = deepcopy(results)

                    else:

                        logger.info(f"Applying validation E{code}: \"{func.__name__}\"; target={dataset}.")

                        # Execute validation and store non-empty results.
                        results = func(dataset)
                        if len(results["values"]):
                            self.errors[f"E{code} - {dataset} - {desc}"] = deepcopy(results)

        except (KeyError, SyntaxError, ValueError) as e:
            logger.exception("Unable to apply validation.")
            logger.exception(e)
            sys.exit(1)

    def connectivity_min_distance(self, dataset: str) -> dict:
        """
        Validates: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Compile all non-duplicated nodes (dead ends) as a DataFrame.
        pts = df["pt_start"].append(df["pt_end"])
        deadends = pts.loc[~pts.duplicated(keep=False)]
        deadends = pd.DataFrame({"pt": deadends.values, self.id: deadends.index})

        # Generate simplified node buffers with distance tolerance.
        deadends["buffer"] = deadends["pt"].map(lambda pt: Point(pt).buffer(self._min_dist, resolution=5))

        # Query arcs which intersect each dead end buffer.
        deadends["intersects"] = deadends["buffer"].map(
            lambda buffer: set(df.sindex.query(buffer, predicate="intersects")))

        # Flag dead ends which have buffers with one or more intersecting arcs.
        deadends = deadends.loc[deadends["intersects"].map(len) > 1]
        if len(deadends):

            # Aggregate deadends to their source features.
            # Note: source features will exist twice if both nodes are deadends; these results will be aggregated.
            deadends_agg = helpers.groupby_to_list(deadends, self.id, "intersects") \
                .map(chain.from_iterable).map(set).to_dict()
            deadends["intersects"] = deadends[self.id].map(deadends_agg)
            deadends.drop_duplicates(subset=self.id, inplace=True)

            # Compile identifiers corresponding to each 'intersects' index.
            deadends["intersects"] = deadends["intersects"].map(
                lambda idxs: set(itemgetter(*idxs)(self.idx_id_lookup[dataset])))

            # Compile identifiers containing either of the source geometry nodes.
            deadends["connected"] = deadends[self.id].map(
                lambda identifier: set(chain.from_iterable(
                    itemgetter(node)(self.pts_id_lookup[dataset]) for node in itemgetter(0, -1)(
                        itemgetter(identifier)(df["pts_tuple"]))
                )))

            # Subtract identifiers of connected features from buffer-intersecting features.
            deadends["disconnected"] = deadends["intersects"] - deadends["connected"]

            # Filter to those results with disconnected segments.
            flag = deadends["disconnected"].map(len) > 0
            if sum(flag):

                # Remove duplicated results.
                deadends = deadends.loc[flag]
                deadends["ids"] = deadends[[self.id, "disconnected"]].apply(
                    lambda row: tuple({row[0], *row[1]}), axis=1)
                deadends.drop_duplicates(subset="ids", keep="first", inplace=True)

                # Compile error logs.
                errors["values"] = deadends["ids"].map(
                    lambda ids: f"Disconnected features are too close: {*ids,}".replace(",)", ")")).to_list()
                vals = set(chain.from_iterable(deadends["ids"]))
                errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def connectivity_node_intersection(self, dataset: str) -> dict:
        """
        Validates: Arcs must only connect at endpoints (nodes).

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Compile nodes.
        nodes = set(df["pt_start"].append(df["pt_end"]))

        # Compile interior vertices (non-nodes).
        # Note: only arcs with > 2 vertices are used.
        non_nodes = set(df.loc[df["pts_tuple"].map(len) > 2, "pts_tuple"]
                        .map(lambda pts: set(pts[1:-1])).map(tuple).explode())

        # Compile invalid vertices.
        invalid_pts = nodes.intersection(non_nodes)

        # Filter invalid vertices to those with multiple connected features.
        invalid_pts = set(compress(invalid_pts,
                                   map(lambda pt: len(itemgetter(pt)(self.pts_id_lookup[dataset])) > 1, invalid_pts)))
        if len(invalid_pts):

            # Filter arcs to those with an invalid vertex.
            invalid_ids = set(chain.from_iterable(map(lambda pt: itemgetter(pt)(self.pts_id_lookup[dataset]),
                                                      invalid_pts)))
            df = df.loc[df.index.isin(invalid_ids)]

            # Flag invalid segments where the invalid vertex is a non-node.
            flag = df["pts_tuple"].map(lambda pts: len(set(pts[1:-1]).intersection(invalid_pts))) > 0
            if sum(flag):

                # Compile error logs.
                vals = set(df.loc[flag].index)
                errors["values"] = vals
                errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            coord_dist = coord_pairs.map(lambda pair: math.dist(*pair))

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
                errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            default = self.defaults_all[dataset]["structtype"]
            structures = df.loc[~df["structtype"].isin({default, "None"})]

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
                errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def dates_combination(self, dataset: str, col: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a valid YYYYMMDD combination.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[df[col] != default, col].copy(deep=True)

        # Define length-dependant datetime strftime formats.
        strftime = {4: "%Y", 6: "%Y%m", 8: "%Y%m%d"}

        # Iterate valid lengths.
        for length in (4, 6, 8):
            series_ = series.loc[series.map(lambda val: int(math.log10(val)) + 1) == length].copy(deep=True)

            # Flag records with invalid YYYYMMDD combination.
            flag = pd.to_datetime(series_, format=strftime[length], errors="coerce").isna()
            if sum(flag):

                # Compile error logs.
                vals = set(series_.loc[flag].index)
                errors["values"].update(vals)

        # Compile error log query.
        if len(errors["values"]):
            errors["query"] = f"\"{self.id}\" in {*errors['values'],}".replace(",)", ")")

        return errors

    def dates_length(self, dataset: str, col: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using
            zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[df[col] != default, col].copy(deep=True)

        # Flag records with an invalid length.
        flag = ~series.map(lambda val: int(math.log10(val)) + 1).isin({4, 6, 8})
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def dates_range(self, dataset: str, col: str) -> dict:
        """
        Validates: Attributes \"credate\" and \"revdate\" must be between 19600101 and the current date, inclusively.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[df[col] != default, col].copy(deep=True)

        # Fetch current date.
        today = int(datetime.today().strftime("%Y%m%d"))

        # Temporary populate incomplete dates with "01" suffix.
        for length in (4, 6):
            flag = series.map(lambda val: int(math.log10(val)) + 1) == length
            if length == 4:
                series.loc[flag] = series.loc[flag].map(lambda val: (val * 10000) + 101)
            else:
                series.loc[flag] = series.loc[flag].map(lambda val: (val * 100) + 1)

        # Flag records with invalid range.
        flag = ~series.between(left=19600101, right=today, inclusive="both")
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def duplication_duplicated(self, dataset: str) -> dict:
        """
        Validates: Features within the same dataset must not be duplicated.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}
        dups = pd.Series()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # LineStrings.
        if df.geom_type.iloc[0] == "LineString":

            # Filter arcs to those with duplicated lengths.
            df = df.loc[df.length.duplicated(keep=False)]
            if len(df):

                # Filter arcs to those with duplicated nodes.
                df = df.loc[df[["pt_start", "pt_end"]].agg(set, axis=1).map(tuple).duplicated(keep=False)]

                # Flag duplicated geometries.
                dups = df.loc[df["geometry"].map(lambda g1: df["geometry"].map(lambda g2: g1.equals(g2)).sum() > 1)]

        # Points.
        else:

            # Extract points.
            pts = df["geometry"].map(lambda g: itemgetter(0)(attrgetter("coords")(g)))

            # Flag duplicated geometries.
            dups = pts.loc[pts.duplicated(keep=False)]

        # Compile error logs.
        if len(dups):

            vals = set(dups.index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def encoding_(self, dataset: str, col: str) -> dict:
        """
        Validates: Attribute contains one or more question mark (\"?\"), which may be the result of invalid character
            encoding.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-none values.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, "None"}), col].copy(deep=True)

        # Flag records containing a question mark ("?").
        flag = series.str.contains("?", regex=False)
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def exit_numbers_nid(self, dataset: str) -> dict:
        """
        Validates: Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all arcs
            sharing an NID.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to records with duplicated nids and non-default and non-none exitnbr.
        default = self.defaults_all[dataset]["exitnbr"]
        df = df.loc[(df["nid"].duplicated(keep=False)) & ~(df["exitnbr"].isin({default, "None"}))].copy(deep=True)
        if len(df):

            # Group exitnbrs by nid, removing duplicates.
            nid_exitnbrs = helpers.groupby_to_list(df, group_field="nid", list_field="exitnbr").map(set)

            # Compile nids with multiple exitnbrs.
            invalid_nids = set(nid_exitnbrs.loc[nid_exitnbrs.map(len) > 1].index)
            if len(invalid_nids):

                # Compile error logs.
                vals = set(df.loc[df["nid"].isin(invalid_nids)].index)
                errors["values"] = vals
                errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Compile exitnbr default and valid roadclass values.
        default_exitnbr = self.defaults_all[dataset]["exitnbr"]
        valid_roadclass = {"Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service lane"}

        # Flag records with non-default and non-none exitnbr and roadclass not in the valid list.
        flag = ~(df["exitnbr"].isin({default_exitnbr, "None"})) & ~(df["roadclass"].isin(valid_roadclass))
        if sum(flag):

            # Compile error logs.
            vals = set(df.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def ferry_integration_(self, dataset: str) -> dict:
        """
        Validates: Ferry arcs must be connected to a road arc at at least one of their nodes.

        :param str dataset: name of the dataset to be validated.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframes.
        ferryseg = self.dfs[dataset].copy(deep=True)
        roadseg = self.dfs["roadseg"].copy(deep=True)

        # Compile nodes.
        nodes_ferryseg = set(ferryseg["pt_start"].append(ferryseg["pt_end"]))
        nodes_roadseg = set(roadseg["pt_start"].append(roadseg["pt_end"]))

        # Compile invalid ferry nodes.
        invalid_nodes = nodes_ferryseg.difference(nodes_roadseg)
        if len(invalid_nodes):

            # Filter and compile identifiers of ferries with an invalid node.
            invalid_ids = set(chain.from_iterable(map(lambda node: itemgetter(node)(self.pts_id_lookup[dataset]),
                                                      invalid_nodes)))
            if len(invalid_ids):

                # Compile error logs.
                errors["values"] = invalid_ids
                errors["query"] = f"\"{self.id}\" in {*invalid_ids,}".replace(",)", ")")

        return errors

    def identifiers_32hex(self, dataset: str, col: str) -> dict:
        """
        Validates: IDs must be 32 digit hexadecimal strings.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-none values, excluding nids.
        if col == "nid":
            series = df[col].copy(deep=True)
        else:
            default = self.defaults_all[dataset][col]
            series = df.loc[~df[col].isin({default, "None"}), col].copy(deep=True)

        # Compile hexadecimal characters.
        hexdigits = set(string.hexdigits)

        # Flag records with non-hexadecimal or non-32 digit identifiers.
        series = series.astype(str)
        flag = (series.map(len) != 32) | (series.map(lambda val: not set(val).issubset(hexdigits)))
        if sum(flag):

            # Compile error logs.
            vals = set(series.loc[flag].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors

    def identifiers_nid_linkages(self, dataset: str, col: str) -> dict:
        """
        Validates: NID linkages must be valid.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return dict: dict containing error messages and, optionally, a query to identify erroneous records.
        """

        errors = {"values": set(), "query": None}

        # Configure dataset nid linkages.
        linkages = {
            "addrange":
                {
                    "roadseg": {"adrangenid"}
                },
            "altnamlink":
                {
                    "addrange": {"l_altnanid", "r_altnanid"}
                },
            "roadseg":
                {
                    "blkpassage": {"roadnid"},
                    "tollpoint": {"roadnid"}
                },
            "strplaname":
                {
                    "addrange": {"l_offnanid", "r_offnanid"},
                    "altnamlink": {"strnamenid"}
                }
        }

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-none values.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, "None"}), col].copy(deep=True)

        # Iterate datasets whose nids the current dataset links to.
        for nid_dataset in filter(lambda name: dataset in linkages[name], set(linkages).intersection(self.dfs)):

            # Check if the current column links to the nids of the linked dataset.
            if col in linkages[nid_dataset][dataset]:

                # Compile linked nids.
                nids = set(self.dfs[nid_dataset]["nid"])

                # Flag missing identifiers.
                flag = ~series.isin(nids)
                if sum(flag):

                    # Compile error logs.
                    vals = set(series.loc[flag].index)
                    errors["values"] = vals
                    errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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

        # Compile indexes of geometries not completely within the source region.
        invalid_idxs = list(set(range(len(df))) - set(df.sindex.query(self.boundary, predicate="contains")))
        if len(invalid_idxs):

            # Compile error logs.
            vals = set(df.iloc[invalid_idxs].index)
            errors["values"] = vals
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

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
            errors["query"] = f"\"{self.id}\" in {*vals,}".replace(",)", ")")

        return errors
