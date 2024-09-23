import geopandas as gpd
import logging
import math
import pandas as pd
import sys
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from itertools import chain
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely import Point
from tqdm import trange
from typing import Dict, Union

filepath = Path(__file__).resolve()
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from utils import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Validator:
    """Handles the execution of validation functions against the NRN datasets."""

    def __init__(self, dfs: Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]], source: str) -> None:
        """
        Initializes variables for validation functions.

        :param str source: abbreviation for the source province / territory.
        :param Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]] dfs: dictionary of NRN datasets as (Geo)DataFrames.
        """

        self.errors = defaultdict(dict)
        self.source = source
        self.id = "uuid"
        self.to_crs = "EPSG:3348"
        self.dst = filepath.parents[2] / f"data/interim/{self.source}.gpkg"

        # Compile datasets reprojected to a meter-based crs.
        self.dfs = {name: df.to_crs(self.to_crs).copy(deep=True) if "geometry" in df.columns else df.copy(deep=True)
                    for name, df in dfs.items()}

        # Compile default field values.
        self.defaults_all = helpers.compile_default_values()

        logger.info("Configuring validations.")

        # Define validation thresholds.
        self._min_len = 1
        self._min_dist = 5

        # Define validation.
        # Note: List validations in order if execution order matters.
        self.validations = {
            101: {
                "func": self.construction_min_length,
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            102: {
                "func": self.construction_zero_length,
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            103: {
                "func": self.construction_simple,
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            201: {
                "func": self.duplication_duplicated,
                "datasets": ["blkpassage", "ferryseg", "roadseg", "tollpoint"],
                "iter_cols": None
            },
            202: {
                "func": self.duplication_overlap,
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            301: {
                "func": self.connectivity_min_distance,
                "datasets": ["ferryseg", "roadseg"],
                "iter_cols": None
            },
            401: {
                "func": self.dates_length,
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            402: {
                "func": self.dates_combination,
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            403: {
                "func": self.dates_range,
                "datasets": ["addrange", "blkpassage", "ferryseg", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": ["credate", "revdate"]
            },
            501: {
                "func": self.identifiers_nid_linkages,
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
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            602: {
                "func": self.exit_numbers_roadclass,
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            701: {
                "func": self.ferry_integration_,
                "datasets": ["ferryseg"],
                "iter_cols": None
            },
            801: {
                "func": self.number_of_lanes_,
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            901: {
                "func": self.speed_,
                "datasets": ["roadseg"],
                "iter_cols": None
            },
            1001: {
                "func": self.encoding_,
                "datasets": ["addrange", "blkpassage", "ferryseg", "junction", "roadseg", "strplaname", "tollpoint"],
                "iter_cols": {name: set(df.select_dtypes(include="object").columns) - {"geometry", "nid", "uuid"} for
                              name, df in self.dfs.items()}
            }
        }

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
        for dataset in {"ferryseg", "roadseg"}.intersection(set(self.dfs)):
            df = self.dfs[dataset].copy(deep=True)

            # Generate computationally intensive geometry attributes as new columns.
            df["pts_tuple"] = df["geometry"].map(attrgetter("coords")).map(tuple)
            df["pt_start"] = df["pts_tuple"].map(itemgetter(0))
            df["pt_end"] = df["pts_tuple"].map(itemgetter(-1))

            # Generate computationally intensive lookups.
            pts = df["pts_tuple"].explode()
            pts_df = pd.DataFrame({"pt": pts.values, self.id: pts.index})
            self.pts_id_lookup[dataset] = deepcopy(pts_df[["pt", self.id]]
                                                   .groupby(by="pt", as_index=True)[self.id].agg(set).to_dict())
            self.idx_id_lookup[dataset] = deepcopy(dict(zip(range(len(df)), df.index)))

            # Store updated dataframe.
            self.dfs[dataset] = df.copy(deep=True)

    def __call__(self) -> None:
        """Orchestrates the execution of validation functions and compiles the resulting errors."""

        logger.info("Applying validations.")

        try:

            # Iterate validations.
            for code, params in self.validations.items():
                func, datasets, iter_cols = itemgetter("func", "datasets", "iter_cols")(params)

                # Configure valid datasets.
                datasets = set(datasets).intersection(self.dfs)

                # Reconfigure iter_cols as dict.
                if isinstance(iter_cols, list):
                    iter_cols = {dataset: iter_cols for dataset in datasets}

                # Instantiate progress bar.
                pbar = trange(sum(map(len, itemgetter(*datasets)(iter_cols))) if iter_cols else len(datasets),
                              desc="Applying validations.", bar_format="{desc}|{bar}| {percentage:3.0f}% {r_bar}")

                # Iterate datasets.
                for dataset in datasets:

                    # Create entry for error.
                    self.errors[code][dataset] = set()

                    # Iterate columns, if required.
                    if iter_cols:

                        for col in iter_cols[dataset]:

                            pbar.set_description(f"Applying validation {code}: \"{func.__name__}\". Current target: "
                                                 f"{dataset}.{col}")

                            # Execute validation and store results.
                            self.errors[code][dataset].update(deepcopy(func(dataset, col=col)))

                            # Update progress bar.
                            pbar.update(1)

                    else:

                        pbar.set_description(f"Applying validation {code}: \"{func.__name__}\". Current target: "
                                             f"{dataset}")

                        # Execute validation and store results.
                        self.errors[code][dataset].update(deepcopy(func(dataset)))

                        # Update progress bar.
                        pbar.update(1)

                # Close progress bar.
                pbar.close()

        except (KeyError, SyntaxError, ValueError) as e:
            logger.exception("Unable to apply validation.")
            logger.exception(e)
            sys.exit(1)

    def connectivity_min_distance(self, dataset: str) -> set:
        f"""
        Validates: Arcs must be >= {self._min_dist} meter{'s' if self._min_dist > 1 else ''} from each other, excluding 
        connected arcs (i.e. no dangles).

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Compile all non-duplicated nodes (dead ends) as a DataFrame.
        pts = pd.concat([df["pt_start"], df["pt_end"]])
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
            deadends_agg = deadends[[self.id, "intersects"]].groupby(by=self.id, as_index=True)["intersects"]\
                .agg(tuple).map(chain.from_iterable).map(set).to_dict()
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

            # Compile error logs.
            if sum(flag):
                errors.update(set(deadends.loc[flag, self.id]))

        return errors

    def construction_min_length(self, dataset: str) -> set:
        f"""
        Validates: Arcs must be >= {self._min_len} meter{'s' if self._min_len > 1 else ''} in length, except structures 
        (e.g. Bridges).

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

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
            structure_nodes = pd.concat([structures["pt_start"], structures["pt_end"]])
            structure_nodes_dups = set(structure_nodes.loc[structure_nodes.duplicated(keep=False)])

            # Flag isolated structures.
            isolated_structure_index = set(structures.loc[~((structures["pt_start"].isin(structure_nodes_dups)) |
                                                            (structures["pt_end"].isin(structure_nodes_dups)))].index)
            isolated_structure_flag = df.index.isin(isolated_structure_index)

            # Modify flag to exclude isolated structures.
            flag = (flag & (~isolated_structure_flag))

            # Compile error logs.
            if sum(flag):
                errors.update(set(df.loc[flag].index))

        return errors

    def construction_simple(self, dataset: str) -> set:
        """
        Validates: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Flag complex (non-simple) geometries.
        flag = ~df.is_simple

        # Compile error logs.
        if sum(flag):
            errors.update(set(df.loc[flag].index))

        return errors

    def construction_zero_length(self, dataset: str) -> set:
        """
        Validates: Arcs must not have zero length.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Flag arcs which are too short.
        flag = df.length == 0

        # Compile error logs.
        if sum(flag):
            errors.update(set(df.loc[flag].index))

        return errors

    def dates_combination(self, dataset: str, col: str) -> set:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have a valid YYYYMMDD combination.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-zero dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, 0}), col].copy(deep=True)

        # Define length-dependant datetime strftime formats.
        strftime = {4: "%Y", 6: "%Y%m", 8: "%Y%m%d"}

        # Iterate valid lengths.
        for length in (4, 6, 8):
            series_ = series.loc[series.map(lambda val: int(math.log10(val)) + 1) == length].copy(deep=True)

            # Flag records with invalid YYYYMMDD combination.
            flag = pd.to_datetime(series_, format=strftime[length], errors="coerce").isna()

            # Compile error logs.
            if sum(flag):
                errors.update(set(series_.loc[flag].index))

        return errors

    def dates_length(self, dataset: str, col: str) -> set:
        """
        Validates: Attributes \"credate\" and \"revdate\" must have lengths of 4, 6, or 8. Therefore, using
            zero-padded digits, dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-zero dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, 0}), col].copy(deep=True)

        # Flag records with an invalid length.
        flag = ~series.map(lambda val: int(math.log10(val)) + 1).isin({4, 6, 8})

        # Compile error logs.
        if sum(flag):
            errors.update(set(series.loc[flag].index))

        return errors

    def dates_range(self, dataset: str, col: str) -> set:
        """
        Validates: Attributes \"credate\" and \"revdate\" must be between 19600101 and the current date, inclusively.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-zero dates.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, 0}), col].copy(deep=True)

        # Fetch current date.
        today = int(datetime.today().strftime("%Y%m%d"))

        # Temporarily populate incomplete dates with "01" suffix.
        # Note: Requires casting to int64.
        series = series.astype("int64")

        for length in (4, 6):
            flag = series.map(lambda val: int(math.log10(val)) + 1) == length
            if length == 4:
                series.loc[flag] = series.loc[flag].map(lambda val: (val * 10000) + 101)
            else:
                series.loc[flag] = series.loc[flag].map(lambda val: (val * 100) + 1)

        # Flag records with invalid range.
        flag = ~series.between(left=19600101, right=today, inclusive="both")

        # Compile error logs.
        if sum(flag):
            errors.update(set(series.loc[flag].index))

        return errors

    def duplication_duplicated(self, dataset: str) -> set:
        """
        Validates: Features within the same dataset must not be duplicated.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()
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
            errors.update(set(dups.index))

        return errors

    def duplication_overlap(self, dataset: str) -> set:
        """
        Validates: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Query arcs which overlap each segment.
        overlaps = df["geometry"].map(lambda g: set(df.sindex.query(g, predicate="overlaps")))

        # Flag arcs which have one or more overlapping segments.
        flag = overlaps.map(len) > 0

        # Compile error logs.
        if sum(flag):
            errors.update(set(overlaps.loc[flag].index))

        return errors

    def encoding_(self, dataset: str, col: str) -> set:
        """
        Validates: Attribute contains one or more question mark (\"?\"), which may be the result of invalid character
            encoding.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default and non-none values.
        default = self.defaults_all[dataset][col]
        series = df.loc[~df[col].isin({default, "None"}), col].copy(deep=True)

        # Flag records containing a question mark ("?").
        flag = series.str.contains("?", regex=False)

        # Compile error logs.
        if sum(flag):
            errors.update(set(series.loc[flag].index))

        return errors

    def exit_numbers_nid(self, dataset: str) -> set:
        """
        Validates: Attribute \"exitnbr\" must be identical, excluding the default value or \"None\", for all arcs
            sharing an NID.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to records with duplicated nids and non-default and non-none exitnbr.
        default = self.defaults_all[dataset]["exitnbr"]
        df = df.loc[(df["nid"].duplicated(keep=False)) & ~(df["exitnbr"].isin({default, "None"}))].copy(deep=True)
        if len(df):

            # Group exitnbrs by nid, removing duplicates.
            nid_exitnbrs = df[["nid", "exitnbr"]].groupby(by="nid", as_index=True)["exitnbr"].agg(set)

            # Compile nids with multiple exitnbrs.
            invalid_nids = set(nid_exitnbrs.loc[nid_exitnbrs.map(len) > 1].index)

            # Flag records with an invalid nid.
            flag = df["nid"].isin(invalid_nids)

            # Compile error logs.
            if sum(flag):
                errors.update(set(df.loc[flag].index))

        return errors

    def exit_numbers_roadclass(self, dataset: str) -> set:
        """
        Validates: When attribute \"exitnbr\" is not equal to the default value or \"None\", attribute \"roadclass\"
            must equal one of the following: \"Expressway / Highway\", \"Freeway\", \"Ramp\", \"Rapid Transit\",
            \"Service Lane\".

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Compile exitnbr default and valid roadclass values.
        default_exitnbr = self.defaults_all[dataset]["exitnbr"]
        valid_roadclass = {"Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service lane"}

        # Flag records with non-default and non-none exitnbr and roadclass not in the valid list.
        flag = ~(df["exitnbr"].isin({default_exitnbr, "None"})) & ~(df["roadclass"].isin(valid_roadclass))

        # Compile error logs.
        if sum(flag):
            errors.update(set(df.loc[flag].index))

        return errors

    def ferry_integration_(self, dataset: str) -> set:
        """
        Validates: Ferry arcs must be connected to a road arc at at least one of their nodes.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframes.
        ferryseg = self.dfs[dataset].copy(deep=True)
        roadseg = self.dfs["roadseg"].copy(deep=True)

        # Compile nodes.
        nodes_ferryseg = set(pd.concat([ferryseg["pt_start"], ferryseg["pt_end"]]))
        nodes_roadseg = set(pd.concat([roadseg["pt_start"], roadseg["pt_end"]]))

        # Compile invalid ferry nodes.
        invalid_nodes = nodes_ferryseg.difference(nodes_roadseg)
        if len(invalid_nodes):

            # Compile ids of records where both nodes are invalid.
            invalid_ids = set(ferryseg.loc[(ferryseg["pt_start"].isin(invalid_nodes)) &
                                           (ferryseg["pt_end"].isin(invalid_nodes))].index)

            # Compile error logs.
            errors.update(invalid_ids)

        return errors

    def identifiers_nid_linkages(self, dataset: str, col: str) -> set:
        """
        Validates: NID linkages must be valid.

        :param str dataset: name of the dataset to be validated.
        :param str col: column name.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

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

                # Compile error logs.
                if sum(flag):
                    errors.update(set(series.loc[flag].index))

        return errors

    def number_of_lanes_(self, dataset: str) -> set:
        """
        Validates: Attribute \"nbrlanes\" must be between 1 and 8, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset]["nbrlanes"]
        series = df.loc[df["nbrlanes"] != default, "nbrlanes"].copy(deep=True)

        # Flag records with invalid values.
        flag = ~series.between(left=1, right=8, inclusive="both")

        # Compile error logs.
        if sum(flag):
            errors.update(set(series.loc[flag].index))

        return errors

    def speed_(self, dataset: str) -> set:
        """
        Validates: Attribute \"speed\" must be between 5 and 120, inclusively.

        :param str dataset: name of the dataset to be validated.
        :return set: set containing identifiers of erroneous records.
        """

        errors = set()

        # Fetch dataframe.
        df = self.dfs[dataset].copy(deep=True)

        # Filter to non-default dates.
        default = self.defaults_all[dataset]["speed"]
        series = df.loc[df["speed"] != default, "speed"].copy(deep=True)

        # Flag records with invalid values.
        flag = ~series.between(left=5, right=120, inclusive="both")

        # Compile error logs.
        if sum(flag):
            errors.update(set(series.loc[flag].index))

        return errors
