import calendar
import geopandas as gpd
import logging
import networkx as nx
import numpy as np
import pandas as pd
import pyproj
import shapely.ops
import string
import sys
from collections import Counter, defaultdict
from datetime import datetime
from itertools import chain, combinations, compress, groupby, product, tee
from operator import attrgetter, itemgetter
from pathlib import Path
from scipy.spatial import cKDTree
from scipy.spatial.distance import euclidean
from shapely.geometry import Point
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

    def __init__(self, dframes: Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]]) -> None:
        """
        Initializes variables for validation functions.

        :param Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]] dframes: dictionary of NRN dataset names and
            (Geo)DataFrames.
        """

        logger.info("Configuring validation variables.")

        self.errors = defaultdict(list)

        # Compile default field values and dtypes.
        self.defaults_all = helpers.compile_default_values()
        self.dtypes_all = helpers.compile_dtypes()

        # Classify dataframes by geometry type.
        self.df_lines = ("ferryseg", "roadseg")
        self.df_points = ("blkpassage", "junction", "tollpoint")

        # Compile dataframes in original and meter-based projections (EPSG:3348; spatial datasets only).
        self.dframes = dict()
        self.dframes_m = dict()

        for name, df in dframes.items():

            # Store original dataframe.
            self.dframes[name] = df.copy(deep=True)

            # Store reprojected dataframe.
            if "geometry" in df.columns:
                epsg = df.crs.to_epsg()
                if epsg == 3348:
                    self.dframes_m[name] = df.copy(deep=True)
                else:
                    self.dframes_m[name] = df.to_crs("EPSG:3348").copy(deep=True)

        # Define projection transformers, if required.
        self.prj_3348_to_4617 = pyproj.Transformer.from_crs(pyproj.CRS("EPSG:3348"), pyproj.CRS("EPSG:4617"),
                                                            always_xy=True).transform

        # Define validation parameters.
        # Note: List validations in order if execution order matters.
        self.validations = {
            self.duplicated_lines: {
                "code": 1,
                "datasets": self.df_lines,
                "iterate": True
            },
            self.duplicated_points: {
                "code": 2,
                "datasets": self.df_points,
                "iterate": True
            },
            self.isolated_lines: {
                "code": 3,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.dates: {
                "code": 4,
                "datasets": self.dframes.keys(),
                "iterate": True
            },
            self.deadend_proximity: {
                "code": 5,
                "datasets": ["junction", "roadseg"],
                "iterate": False
            },
            self.conflicting_exitnbrs: {
                "code": 6,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.exitnbr_roadclass_relationship: {
                "code": 7,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.ferry_road_connectivity: {
                "code": 8,
                "datasets": ["ferryseg", "roadseg", "junction"],
                "iterate": False
            },
            self.ids: {
                "code": 9,
                "datasets": self.dframes.keys(),
                "iterate": True
            },
            self.line_internal_clustering: {
                "code": 10,
                "datasets": self.df_lines,
                "iterate": True
            },
            self.line_length: {
                "code": 11,
                "datasets": self.df_lines,
                "iterate": True
            },
            self.line_merging_angle: {
                "code": 12,
                "datasets": self.df_lines,
                "iterate": True
            },
            self.line_proximity: {
                "code": 13,
                "datasets": self.df_lines,
                "iterate": True
            },
            self.nbrlanes: {
                "code": 14,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.nid_linkages: {
                "code": 15,
                "datasets": self.dframes.keys(),
                "iterate": True
            },
            self.conflicting_pavement_status: {
                "code": 16,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.point_proximity: {
                "code": 17,
                "datasets": self.df_points,
                "iterate": True
            },
            self.structure_attributes: {
                "code": 18,
                "datasets": ["roadseg", "junction"],
                "iterate": False
            },
            self.roadclass_rtnumber_relationship: {
                "code": 19,
                "datasets": ["ferryseg", "roadseg"],
                "iterate": True
            },
            self.self_intersecting_elements: {
                "code": 20,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.self_intersecting_structures: {
                "code": 21,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.route_contiguity: {
                "code": 22,
                "datasets": ["roadseg"],
                "iterate": False
            },
            self.speed: {
                "code": 23,
                "datasets": ["roadseg"],
                "iterate": True
            },
            self.encoding: {
                "code": 24,
                "datasets": self.dframes.keys(),
                "iterate": True
            },
            self.out_of_scope: {
                "code": 25,
                "datasets": {*self.df_lines, *self.df_points} - {"junction"},
                "iterate": True
            }
        }

    def conflicting_exitnbrs(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to exitnbr field.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]
        default = self.defaults_all[name]["exitnbr"]

        # Query multi-segment road elements (via nid field) where exitnbr is not the default value or not "None".
        df_filtered = df.loc[(df["nid"].duplicated(keep=False)) &
                             (df["nid"] != default) &
                             (~df["exitnbr"].isin({default, "None"}))]

        if len(df_filtered):

            # Group exitnbrs by nid, removing duplicate values.
            grouped = helpers.groupby_to_list(df_filtered, "nid", "exitnbr").map(np.unique)

            # Validation: ensure road element has <= 1 unique exitnbr.
            flag_nids = grouped.loc[grouped.map(len) > 1]

            # Compile error properties.
            for nid, exitnbrs in flag_nids.iteritems():
                exitnbrs = ", ".join(map(lambda val: f"'{val}'", exitnbrs))
                errors[1].append(f"nid '{nid}' has multiple exitnbrs: {exitnbrs}.")

        return errors

    def conflicting_pavement_status(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to pavstatus, pavsurf, and unpavsurf fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Subset dataframe to non-default values, keep only required fields.
        default = self.defaults_all[name]["pavstatus"]
        df_filtered = df.loc[df["pavstatus"] != default, ["pavstatus", "pavsurf", "unpavsurf"]]

        # Apply validations and compile uuids of flagged records.
        if len(df_filtered):

            # Validation: when pavstatus == "Paved", ensure pavsurf != "None" and unpavsurf == "None".
            paved = df_filtered.loc[df_filtered["pavstatus"] == "Paved"]
            errors[1] = paved.loc[paved["pavsurf"] == "None"].index.values
            errors[2] = paved.loc[paved["unpavsurf"] != "None"].index.values

            # Validation: when pavstatus == "Unpaved", ensure pavsurf == "None" and unpavsurf != "None".
            unpaved = df_filtered.loc[df_filtered["pavstatus"] == "Unpaved"]
            errors[3] = unpaved.loc[unpaved["pavsurf"] != "None"].index.values
            errors[4] = unpaved.loc[unpaved["unpavsurf"] == "None"].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def dates(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to credate and revdate fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]
        defaults = helpers.compile_default_values()[name]
        df = df[["credate", "revdate"]].copy(deep=True)

        # Get current date.
        today = datetime.today().strftime("%Y%m%d")
        today = {"year": int(today[:4]), "month": int(today[4:6]), "day": int(today[6:8]), "full": int(today)}

        # Define functions.
        def validate_day(date: int) -> bool:
            """
            Validate the day value in a date.

            :param int date: integer date in format YYYYMMDD.
            :return bool: boolean validation of the date.
            """

            date_str = str(date)
            year, month, day = map(int, [date_str[:4], date_str[4:6], date_str[6:8]])
            try:

                if not 1 <= day <= calendar.mdays[month]:
                    if not all([day == 29, month == 2, calendar.isleap(year)]):
                        return False

            # Captures exception raised by an invalid month value, which itself it handled by another validation.
            except IndexError:
                return False

            return True

        # Iterate credate and revdate, applying validations.
        for col in ("credate", "revdate"):

            # Subset to non-default values.
            s_filtered = df.loc[df[col] != defaults[col], col]

            if len(s_filtered):

                # Validation 1: length must be 4, 6, or 8.
                results = s_filtered.loc[s_filtered.map(lambda date: len(str(date)) not in {4, 6, 8})].index.values
                errors[1].extend(results)

                # Subset to valid records only for remaining validations.
                invalid_indexes = list(set(chain.from_iterable(errors.values())))
                s_filtered2 = s_filtered.loc[~s_filtered.index.isin(invalid_indexes)]

                if len(s_filtered2):

                    # Temporarily set missing month and day values to 01.
                    series_mod = s_filtered2.loc[s_filtered2.map(lambda date: len(str(date)) in {4, 6})]
                    if len(series_mod):
                        append_vals = {4: "0101", 6: "01"}
                        s_filtered2.loc[series_mod.index] = series_mod.map(str).map(
                            lambda date: date + append_vals[len(date)]).map(int)
                        df.loc[s_filtered2.index, col] = s_filtered2

                    # Validation 2: valid date - year.
                    results = s_filtered2.loc[~s_filtered2.map(
                        lambda date: 1960 <= int(str(date)[:4]) <= today["year"])].index.values
                    errors[2].extend(results)

                    # Validation 3: valid date - month.
                    results = s_filtered2.loc[~s_filtered2.map(
                        lambda date: 1 <= int(str(date)[4:6]) <= 12)].index.values
                    errors[3].extend(results)

                    # Validation 4: valid date - day.
                    results = s_filtered2.loc[~s_filtered2.map(validate_day)].index.values
                    errors[4].extend(results)

                    # Validation 5: ensure date <= today.
                    results = s_filtered2.loc[s_filtered2.map(lambda date: date > today["full"])].index.values
                    errors[5].extend(results)

        # Validation 6: ensure credate <= revdate.
        df_filtered = df.loc[(df["credate"] != defaults["credate"]) &
                             (df["revdate"] != defaults["revdate"]) &
                             ~(df.index.isin(set(chain.from_iterable(itemgetter(1, 2)(errors)))))]
        if len(df_filtered):
            results = df_filtered.loc[df_filtered["credate"] > df_filtered["revdate"]].index.values
            errors[6].extend(results)

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def deadend_proximity(self, junction: str = "junction", roadseg: str = "roadseg") -> Dict[int, list]:
        """
        Validates the proximity of deadend junctions to disjoint / non-connected road segments.

        :param str junction: NRN dataset name for NRN junction.
        :param str roadseg: NRN dataset name for NRN roadseg.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        # Validation: deadend junctions must be >= 5 meters from disjoint road segments.
        errors = defaultdict(list)
        junction = self.dframes_m[junction]
        roadseg = self.dframes_m[roadseg]

        # Filter junctions to junctype = "Dead End", keep only required fields.
        deadends = junction.loc[junction["junctype"] == "Dead End", "geometry"]
        roadseg = roadseg["geometry"]

        # Compile coordinates (used multiple times).
        deadends = deadends.map(lambda pt: itemgetter(0)(attrgetter("coords")(pt)))
        roadseg = roadseg.map(lambda g: set(attrgetter("coords")(g)))

        # Generate a lookup dict for the index of each roadseg coordinate, mapped to the full range of coordinate
        # indexes for the road segment associated with that coordinate. Therefore, the coordinate identified for
        # exclusion at distance=0 can be associated with, and expanded to include, all other coordinates along that road
        # segment.
        # Process: get the road segment coordinate counts and cumulative counts to generate an index range for each road
        # segment. Stack the results and duplicate the ranges by the coordinate counts. Convert to a dict.
        coords_count = roadseg.map(len)
        coords_idx_cumsum = coords_count.cumsum()
        coords_full_idx_range = np.repeat(list(map(
            lambda indexes: set(range(*indexes)),
            np.column_stack((coords_idx_cumsum - coords_count, coords_idx_cumsum)))),
            coords_count)
        coords_full_idx_range_lookup = dict(zip(range(len(coords_full_idx_range)), coords_full_idx_range))

        # Generate kdtree.
        tree = cKDTree(list(chain.from_iterable(roadseg)))

        # Compile indexes of road segments within 5 meters distance of each deadend.
        proxi_idx_all = deadends.map(lambda deadend: set(chain(*tree.query_ball_point([deadend], r=5))))

        # Compile index of road segment at 0 meters distance from each deadend. These represent the connected roads.
        # Expand indexes to ranges.
        proxi_idx_exclude = deadends.map(lambda deadend: tree.query([deadend])[-1])
        proxi_idx_exclude = proxi_idx_exclude.map(lambda idx: itemgetter(*idx)(coords_full_idx_range_lookup))

        # Filter coincident indexes from all indexes. Keep only non-empty results.
        proxi_idx_keep = proxi_idx_all - proxi_idx_exclude
        proxi_idx_keep = proxi_idx_keep.loc[proxi_idx_keep.map(len) > 0]
        proxi_idx_keep = proxi_idx_keep.map(tuple).explode()

        # Generate a lookup dict for the index of each roadseg coordinate, mapped to the associated uuid.
        coords_idx_uuid_lookup = dict(zip(range(coords_count.sum()), np.repeat(roadseg.index.values, coords_count)))

        # Compile the uuid associated with resulting proximity point indexes for each deadend.
        proxi_results = proxi_idx_keep.map(lambda idx: itemgetter(idx)(coords_idx_uuid_lookup))

        # Compile error properties: calculate min distance measurement between source and target geometries.
        results = pd.Series(proxi_results.items()).map(
            lambda idxs: (itemgetter(idxs[0])(deadends), tuple(itemgetter(idxs[1])(roadseg))))
        distances = results.map(lambda pts: min(map(lambda target_pt: euclidean(pts[0], target_pt), pts[1]))).round(2)

        # Compile and sort final results.
        results = pd.DataFrame({"target": proxi_results.values, "distance": distances.values},
                               index=proxi_results.index).sort_values(by="distance", ascending=True)

        # Compile error properties: store results.
        for vals in results.itertuples(index=True):
            source, target, distance = attrgetter("Index", "target", "distance")(vals)
            errors[1].append(f"junction uuid '{source}' is too close to roadseg uuid '{target}': {distance} meters.")

        return errors

    def duplicated_lines(self, name: str) -> Dict[int, list]:
        """
        Identifies the uuids of duplicate and overlapping line geometries.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes_m[name]

        # Keep only required fields.
        series = df["geometry"]

        # Validation 1: ensure line segments are not duplicated.

        # Filter geometries to those with duplicate lengths.
        s_filtered = series.loc[series.length.duplicated(keep=False)]

        if len(s_filtered):

            # Filter geometries to those with duplicate endpoint coordinates.
            s_filtered = s_filtered.loc[s_filtered.map(
                lambda g: tuple(sorted(itemgetter(0, -1)(g.coords)))).duplicated(keep=False)]

            if len(s_filtered):

                # Identify duplicate geometries.
                dups = s_filtered.loc[s_filtered.map(
                    lambda geom1: s_filtered.map(lambda geom2: geom1.equals(geom2)).sum() > 1)]

                # Configure duplicate groups and their uuids.
                uuid_groups = set(dups.map(
                    lambda geom1: tuple(set(dups.loc[dups.map(lambda geom2: geom1.equals(geom2))].index))).tolist())

                # Compile error properties.
                if len(uuid_groups):
                    for uuid_group in uuid_groups:
                        vals = ", ".join(map(lambda val: f"'{val}'", uuid_group))
                        errors[1].append(f"Duplicated geometries identified for uuids: {vals}.")

        # Validation 2: ensure line segments do not have repeated adjacent points.

        # Filter geometries to those with duplicated coordinates.
        s_filtered = series.loc[series.map(lambda g: len(g.coords) != len(set(g.coords)))]

        if len(s_filtered):

            # Identify geometries with repeated adjacent coordinates.
            mask = s_filtered.map(lambda g: len(g.coords) != len(list(groupby(g.coords))))

            # Compile uuids of flagged records.
            errors[2] = s_filtered.loc[mask].index.values

        # Validation 3: ensure line segments do not overlap (i.e. contain duplicated adjacent points).

        # Extract coordinates from geometries (used multiple times).
        series_coords = series.map(attrgetter("coords")).map(tuple)

        # Create ordered coordinate pairs, sorted.
        coord_pairs = series_coords.map(ordered_pairs).explode()

        # Remove invalid pairs (duplicated adjacent coordinates).
        coord_pairs = coord_pairs.loc[coord_pairs.map(lambda pair: pair[0] != pair[1])]

        # Group uuids of matching pairs.
        coord_pairs_df = coord_pairs.reset_index(drop=False)
        coord_pairs_grouped = helpers.groupby_to_list(coord_pairs_df, "geometry", "uuid")
        coord_pairs_grouped = pd.DataFrame({"pairs": coord_pairs_grouped.index, "uuid": coord_pairs_grouped.values})

        # Filter to duplicated pairs.
        coord_pairs_dup = coord_pairs_grouped.loc[coord_pairs_grouped["uuid"].map(len) > 1]
        if len(coord_pairs_dup):

            # Group duplicated pairs by sorted uuid groups.
            coord_pairs_dup["uuid"] = coord_pairs_dup["uuid"].map(sorted).map(tuple)
            coord_pairs_dup_grouped = helpers.groupby_to_list(coord_pairs_dup, "uuid", "pairs")

            # Compile error properties.
            if len(coord_pairs_dup_grouped):
                for uuid_group, pairs in coord_pairs_dup_grouped.iteritems():
                    vals = ", ".join(map(lambda val: f"'{val}'", uuid_group))
                    errors[3].append(f"{len(pairs)} overlapping segments identified between uuids: {vals}.")

        # Compile error properties.
        for code, vals in errors.items():
            if code in {2} and len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def duplicated_points(self, name: str) -> Dict[int, list]:
        """
        Identifies the uuids of duplicate point geometries.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Extract coordinates of points.
        pts = df["geometry"].map(lambda g: itemgetter(0)(g.coords))

        # Identify duplicated geometries.
        dups = pts.loc[pts.duplicated(keep=False)]

        if len(dups):

            # Configure duplicated groups and their uuids.
            uuid_groups = set(dups.map(
                lambda geom1: tuple(set(dups.loc[dups.map(lambda geom2: geom1.equals(geom2))].index))).tolist())

            # Compile error properties.
            if len(uuid_groups):
                for uuid_group in uuid_groups:
                    vals = ", ".join(map(lambda val: f"'{val}'", uuid_group))
                    errors[1].append(f"Duplicated geometries identified for uuids: {vals}.")

        return errors

    def encoding(self, name: str) -> Dict[int, list]:
        """
        Identifies potential encoding errors within string fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Iterate string columns.
        for col in set(df.select_dtypes(include="object").columns) - {"geometry", "uuid", "nid"}:

            # Validation: identify values containing one or more question mark ("?"), which may be the result of invalid
            # character encoding.

            # Flag invalid records.
            flag = df[col].str.contains("?", regex=False)

            # Compile error properties.
            for uid, val in df.loc[flag, col].iteritems():
                errors[1].append(f"uuid: '{uid}', attribute: '{val}', based on attribute field: {col}.")

        return errors

    def exitnbr_roadclass_relationship(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to exitnbr and roadclass fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Subset dataframe to non-default and non-"None" values, keep only required fields.
        default = self.defaults_all[name]["exitnbr"]
        s_filtered = df.loc[~df["exitnbr"].isin({default, "None"}), "roadclass"]

        if len(s_filtered):

            # Validation: ensure roadclass is one of: "Expressway / Highway", "Freeway", "Ramp", "Rapid Transit",
            #             "Service Lane" when exitnbr is not the default value or not "None".

            # Compile uuids of flagged records.
            errors[1] = s_filtered.loc[~s_filtered.isin(
                {"Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane"})].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def ferry_road_connectivity(self, ferryseg: str = "ferryseg", roadseg: str = "roadseg",
                                junction: str = "junction") -> Dict[int, list]:
        """
        Validates the connectivity between ferry and road line segments.

        :param str ferryseg: NRN dataset name for NRN ferryseg.
        :param str roadseg: NRN dataset name for NRN roadseg.
        :param str junction: NRN dataset name for NRN junction.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)

        # Filter dataframes to only required fields.
        ferryseg = self.dframes[ferryseg]["geometry"]
        roadseg = self.dframes[roadseg]["geometry"]
        junction = self.dframes[junction]

        # Validation 1: ensure ferry segments connect to a road segment at at least one endpoint.

        # Compile junction coordinates where junctype = "Ferry".
        ferry_junctions = list(set(chain([geom.coords[0] for geom in
                                          junction.loc[junction["junctype"] == "Ferry", "geometry"].values])))

        # Identify ferry segments which do not connect to any road segments.
        mask = ferryseg.map(
            lambda geom: not any(coords in ferry_junctions for coords in itemgetter(0, -1)(geom.coords)))

        # Compile uuids of flagged records.
        errors[1] = ferryseg.loc[mask].index.values

        # Validation 2: ensure ferry segments connect to <= 1 road segment at either endpoint.

        # Compile road segments which connect to ferry segments.
        roads_connected = roadseg.loc[roadseg.map(
            lambda geom: any(coords in ferry_junctions for coords in itemgetter(0, -1)(geom.coords)))]

        # Compile coordinates of connected road segments.
        road_coords_count = Counter(chain.from_iterable(roads_connected.map(
            lambda g: tuple(set(itemgetter(0, -1)(g.coords))))))

        # Identify ferry endpoints which intersect multiple road segments.
        ferry_multi_intersect = ferryseg.map(
            lambda ferry: any(itemgetter(coords)(road_coords_count) > 1 for coords in itemgetter(0, -1)(ferry.coords)))

        # Compile uuids of flagged records.
        errors[2] = ferryseg.loc[ferry_multi_intersect].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def ids(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to all id fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]
        dtypes, defaults = self.dtypes_all[name], self.defaults_all[name]

        # Iterate fields which a) end with "id", b) are str type, and c) are not uuid.
        for col in [fld for fld in df.columns.difference(["uuid"]) if fld.endswith("id") and dtypes[fld] == "str"]:

            # Subset dataframe to required column with non-default and non-"None" values.
            series = df.loc[~df[col].isin([defaults[col], "None"]), col]

            if len(series):

                # Validation 1: ensure ids are 32 digits.
                # Compile uuids of flagged records.
                flag_uuids = series.loc[series.map(len) != 32].index.values
                for uid in flag_uuids:
                    errors[1].append(f"uuid: '{uid}', based on attribute field: {col}.")

                # Validation 2: ensure ids are hexadecimal.
                # Compile uuids of flagged records.
                hexdigits = set(string.hexdigits)
                flag_uuids = series.loc[series.map(lambda uid: not set(uid).issubset(hexdigits))].index.values
                for uid in flag_uuids:
                    errors[2].append(f"uuid: '{uid}', based on attribute field: {col}.")

        # Iterate unique id fields.
        unique_fields = {"ferrysegid", "roadsegid"}
        for col in unique_fields.intersection(set(df.columns)):

            # Filter dataframe to required column.
            series = df[col]

            # Validation 3: ensure unique id fields are unique within their column.
            # Compile uuids of flagged records.
            flag_uuids = series.loc[series.duplicated(keep=False)].index.values
            for uid in flag_uuids:
                errors[3].append(f"uuid: '{uid}', based on attribute field: {col}.")

            # Validation 4: ensure unique id fields are not "None" nor the default field value.
            # Compile uuids of flagged records.
            flag_uuids = series.loc[series.isin([defaults[col], "None"])].index.values
            for uid in flag_uuids:
                errors[4].append(f"uuid: '{uid}', based on attribute field: {col}.")

        return errors

    def isolated_lines(self, name: str, junction: str = "junction") -> Dict[int, list]:
        """
        Identifies the uuids of isolated line segments.

        :param str name: NRN dataset name.
        :param str junction: NRN dataset name for NRN junction.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)

        # Filter dataframes to only required fields.
        df = self.dframes[name][["uuid", "geometry"]]
        junction = self.dframes[junction][["junctype", "geometry"]]

        # Validation 1: ensure line segments are connected to at least one other line segment.

        # Compile junctions for 'Dead End'.
        pts = set(chain([geom.coords[0] for geom in
                         junction.loc[junction["junctype"] == "Dead End", "geometry"].values]))

        # Identify isolated segments.
        # Flag records where both endpoints are 'Dead End'.
        mask = df["geometry"].map(lambda g: all(map(lambda pt: pt in pts, itemgetter(0, -1)(g.coords))))

        # Compile uuids of flagged records, compile error properties.
        if sum(mask):
            errors[1] = list(map(lambda val: f"uuid: '{val}'", df.loc[mask].index.values))

        # Validation 2: identify line segments which connect to another line segment at intermediate / non-endpoint
        # vertices.

        # Compile all coordinates and their count from across the entire dataset.
        df_nodes_all = df["geometry"].map(attrgetter("coords")).map(tuple)
        nodes_count = Counter(chain.from_iterable(df_nodes_all.map(set)))

        # Filter analysis records to those with > 2 constituent points.
        df_nodes = df_nodes_all.loc[df_nodes_all.map(len) > 2]

        # Configure duplicated non-endpoints for analysis records relative to the full dataframe.
        def non_endpoint_dups(nodes: Tuple[tuple, ...]) -> Union[None, Tuple[Tuple[tuple, ...], Tuple[int, ...]]]:
            """
            Returns intermediate / non-endpoint nodes and their dataframe counts if they are duplicated.

            :param Tuple[tuple, ...] nodes: tuple of coordinate tuples.
            :return Union[None, Tuple[Tuple[tuple, ...], Tuple[int, ...]]]: None or a nested tuple containing a tuple of
                all non-endpoint coordinate tuples and a tuple of the frequency of each node within the entire dataset.
            """

            counts = itemgetter(*nodes[1:-1])(nodes_count)
            if not isinstance(counts, tuple):
                counts = (counts,)
            counts_valid = tuple(map(lambda count: count > 1, counts))

            if any(counts_valid):
                return tuple(compress(nodes[1:-1], counts_valid)), tuple(compress(counts, counts_valid))
            else:
                return None

        dups = df_nodes.map(non_endpoint_dups)
        dups = dups.loc[~dups.isna()]

        # Nest nodes with counts and explode records.
        dups = dups.map(lambda vals: tuple(zip(*vals))).explode()

        # Compile uuids of flagged records, compile error properties.
        for index, data in dups.iteritems():
            errors[2].append(f"uuid: '{index}' intersects {data[1] - 1} other line segment(s) at non-endpoint vertex: "
                             f"{data[0]}.")

        return errors

    def line_internal_clustering(self, name: str) -> Dict[int, list]:
        """
        Validates the distance between adjacent coordinates of line segments.
        Validation: line segments must have >= 1x10^(-2) (0.01) meters distance between adjacent coordinates.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        min_distance = 0.01
        series = self.dframes_m[name]["geometry"]

        # Extract coordinates from geometries.
        series_coords = series.map(attrgetter("coords")).map(tuple)

        # Filter out records with only 2 constituent points.
        series_coords = series_coords.loc[series_coords.map(len) > 2]
        if len(series_coords):

            # Create ordered coordinate pairs, sorted.
            coord_pairs = series_coords.map(ordered_pairs).explode()

            # Remove invalid pairs (duplicated adjacent coordinates).
            coord_pairs = coord_pairs.loc[coord_pairs.map(lambda pair: pair[0] != pair[1])]

            # Calculate distance between coordinate pairs.
            coord_dist = coord_pairs.map(lambda pair: euclidean(pair[0], pair[-1]))

            # Flag invalid distances and create dataframe with invalid pairs and distances.
            flag = coord_dist < min_distance
            invalid_df = pd.DataFrame({"pair": coord_pairs.loc[flag], "distance": coord_dist.loc[flag]},
                                      index=coord_dist.loc[flag].index)
            if len(invalid_df):

                # Compile error properties.
                for record in invalid_df.sort_values(by=["uuid", "distance"], ascending=True).itertuples(index=True):
                    index, coords, distance = attrgetter("Index", "pair", "distance")(record)

                    # Reproject coordinates back to NRN CRS.
                    coords = [shapely.ops.transform(self.prj_3348_to_4617, Point(pt)).coords[0] for pt in coords]

                    errors[1].append(f"uuid: '{index}', coordinates: {coords[0]} and {coords[1]}, are too close: "
                                     f"{distance} meters.")

        return errors

    def line_length(self, name: str) -> Dict[int, list]:
        """
        Validates the minimum feature length of line geometries.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        min_length = 5
        series = self.dframes_m[name]["geometry"]

        # Validation: ensure line segments are >= 5 meters in length.
        flag = series.length < min_length

        # Compile error properties.
        if sum(flag):
            for index, val in series.loc[flag].length.round(2).sort_values(ascending=True).iteritems():
                errors[1].append(f"uuid: '{index}' is too short: {val} meters.")

        return errors

    def line_merging_angle(self, name: str) -> Dict[int, list]:
        """
        Validates the merging angle of line segments.
        Validation: ensure line segments merge at angles >= 5 degrees.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        # Define function to calculate the angular degrees between two intersecting lines.
        def get_angle(ref_pt: tuple, pt1: tuple, pt2: tuple) -> bool:
            """
            Validates the angle formed by the 2 points and reference point.

            :param tuple ref_pt: coordinate tuple of the reference point.
            :param tuple pt1: coordinate tuple
            :param tuple pt2: coordinate tuple
            :return bool: boolean validation of the angle formed by the 2 points and 1 reference point.
            """

            angle_1 = np.angle(complex(*(np.array(pt1) - np.array(ref_pt))), deg=True)
            angle_2 = np.angle(complex(*(np.array(pt2) - np.array(ref_pt))), deg=True)

            return round(abs(angle_1 - angle_2), 2)

        errors = defaultdict(list)
        merging_angle = 5
        series = self.dframes_m[name]["geometry"]

        # Compile line endpoints and their neighbours, convert to uuid-neighbour lookup dict.
        endpts_nbrs = series.map(
            lambda g: tuple(map(itemgetter(0, 1), itemgetter(0, 1, -2, -1)(attrgetter("coords")(g)))))
        uuid_nbr_lookup = endpts_nbrs.to_dict()

        # Compile only endpoints.
        endpts = endpts_nbrs.map(itemgetter(0, -1))

        # Explode point groups, filter to only duplicates, and construct a dataframe of the uuids and coordinates.
        pts_exploded = endpts.explode()
        pts_dups = pts_exploded.loc[pts_exploded.duplicated(keep=False)]
        pts_df = pd.DataFrame({"coords": pts_dups, "uuid": pts_dups.index})

        # Proceed only if duplicated points exist.
        if len(pts_df):

            # Group uuids according to coordinates. Explode and convert to DataFrame, keeping index as column.
            grouped_pt_uuid = helpers.groupby_to_list(pts_df, "coords", "uuid")
            uuid_pt_df = grouped_pt_uuid.explode().reset_index(drop=False).rename(columns={"index": "pt", 0: "uuid"})

            # Compile endpoint-neighbouring points.
            # Process: Flag uuids according to duplication status within their group. For unique uuids, configure the
            # neighbouring point based on whichever endpoint matches the common group point. For duplicated uuids
            # (which represent self-loops), the first duplicate takes the second point, the second duplicate takes the
            # second-last point - thereby avoiding the same neighbour being taken twice for self-loop intersections.
            dup_flags = {
                "dup_none": uuid_pt_df.loc[~uuid_pt_df.duplicated(keep=False), ["uuid", "pt"]],
                "dup_first": uuid_pt_df.loc[uuid_pt_df.duplicated(keep="first"), "uuid"],
                "dup_last": uuid_pt_df.loc[uuid_pt_df.duplicated(keep="last"), "uuid"]
            }
            dup_results = {
                "dup_none": np.vectorize(
                    lambda uid, pt:
                    itemgetter({True: 1, False: -2}[uuid_nbr_lookup[uid][0] == pt])(uuid_nbr_lookup[uid]),
                    otypes=[tuple])(dup_flags["dup_none"]["uuid"], dup_flags["dup_none"]["pt"]),
                "dup_first": dup_flags["dup_first"].map(lambda uid: uuid_nbr_lookup[uid][1]).values,
                "dup_last": dup_flags["dup_last"].map(lambda uid: uuid_nbr_lookup[uid][-2]).values
            }

            uuid_pt_df["pt_nbr"] = None
            uuid_pt_df.loc[dup_flags["dup_none"].index, "pt_nbr"] = dup_results["dup_none"]
            uuid_pt_df.loc[dup_flags["dup_first"].index, "pt_nbr"] = dup_results["dup_first"]
            uuid_pt_df.loc[dup_flags["dup_last"].index, "pt_nbr"] = dup_results["dup_last"]

            # Aggregate groups of points and associated neighbours.
            grouped_pt_nbrs = helpers.groupby_to_list(uuid_pt_df, "pt", "pt_nbr")

            # Configure all point-neighbour and point-uuid combinations.
            combos_pt_nbrs = grouped_pt_nbrs.map(lambda vals: combinations(vals, r=2)).map(tuple).explode()
            combos_pt_uuid = grouped_pt_uuid.map(lambda vals: combinations(vals, r=2)).map(tuple).explode()

            # Prepend reference point to neighbour point tuples, add uuid combinations as index.
            combos = pd.Series(
                np.vectorize(lambda pt, nbrs: (pt, *nbrs), otypes=[tuple])(combos_pt_nbrs.index, combos_pt_nbrs),
                index=combos_pt_uuid.values)

            # Calculate the merging angle (in degrees) between each set of points. Filter to invalid records.
            angles = combos.map(lambda pts: get_angle(*pts))
            results = angles.loc[angles < merging_angle]

            # Compile error properties.
            if len(results):
                for uuids, angle in results.drop_duplicates().sort_values(ascending=True).iteritems():
                    line1, line2 = itemgetter(0, 1)(uuids)
                    errors[1].append(f"uuids: '{line1}', '{line2}' merge at too small an angle: {angle} degrees.")

        return errors

    def line_proximity(self, name: str) -> Dict[int, list]:
        """
        Validates the proximity of line segments.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        # Validation: ensure line segments are >= 5 meters from each other, excluding connected segments.
        errors = defaultdict(list)
        prox_limit = 5
        series = self.dframes_m[name]["geometry"]

        # Compile all unique segment coordinates.
        pts = series.map(lambda g: list(set(attrgetter("coords")(g))))
        pts_exploded = pts.explode()

        # Generate lookup dicts for:
        # 1) point coordinate to connected segment uuids.
        # 2) point index to segment uuid.
        pts_exploded_df = pd.DataFrame(pts_exploded).reset_index(drop=False)
        pts_uuids_lookup = helpers.groupby_to_list(pts_exploded_df, "geometry", "uuid").to_dict()
        pts_idx_uuid_lookup = pts_exploded_df["uuid"].to_dict()

        # Generate kdtree.
        tree = cKDTree(pts_exploded.to_list())

        # Compile uuids connected to each segment.
        uuids_exclude = pts.map(lambda points: set(chain.from_iterable(itemgetter(*points)(pts_uuids_lookup))))

        # Compile indexes of segment points < 5 meters distance of each segment, retrieve uuids of returned indexes.
        uuids_proxi = pts.map(
            lambda points: set(itemgetter(*chain(*tree.query_ball_point(points, r=prox_limit)))(pts_idx_uuid_lookup)))

        # Remove connected uuids from each set of uuids, keep non-empty results.
        proxi_results = uuids_proxi - uuids_exclude
        proxi_results = proxi_results.loc[proxi_results.map(len) > 0]
        proxi_results = proxi_results.map(list).explode()

        # Reduce duplicated result pairs.
        results = pd.Series(tuple(set(map(lambda vals: tuple(sorted(vals)), proxi_results.items()))))

        # Compile error properties: calculate min distance measurement between source and target geometries.
        distances = results.map(lambda idxs: tuple(product(itemgetter(idxs[0])(pts), itemgetter(idxs[1])(pts)))).map(
            lambda pts: min(map(lambda pair: euclidean(*pair), pts))).round(2)

        # Compile error properties: compile and sort final results.
        results = pd.DataFrame({"target": results.map(itemgetter(1)).values, "distance": distances.values},
                               index=results.map(itemgetter(0)).values).sort_values(by="distance", ascending=True)

        # Compile error properties: store results.
        for vals in results.itertuples(index=True):
            source, target, distance = attrgetter("Index", "target", "distance")(vals)
            errors[1].append(f"uuids: '{source}', '{target}' are too close: {distance} meters.")

        return errors

    def nbrlanes(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to nbrlanes field.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Subset dataframe to non-default values, keep only required fields.
        default = self.defaults_all[name]["nbrlanes"]
        s_filtered = df.loc[df["nbrlanes"] != default, "nbrlanes"]

        if len(s_filtered):

            # Validation: ensure 1 <= nbrlanes <= 8.
            # Compile uuids of flagged records.
            errors[1] = s_filtered.loc[~s_filtered.map(lambda nbrlanes: 1 <= int(nbrlanes) <= 8)].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def nid_linkages(self, name: str) -> Dict[int, list]:
        """
        Validates the nid linkages for the input dataframe, excluding 'None'.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Define nid linkages.
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

        # Iterate nid tables which link to the id table.
        id_table = name
        for nid_table in filter(lambda t: id_table in linkages[t], set(linkages).intersection(self.dframes)):

            # Retrieve nids as lowercase.
            nids = set(self.dframes[nid_table]["nid"].map(str.lower))

            # Iterate linked columns.
            for col in linkages[nid_table][id_table]:

                # Validation: ensure all nid linkages are valid.
                logger.info(f"Validating nid linkage: {nid_table}.nid - {id_table}.{col}.")

                # Retrieve column ids as lowercase.
                ids = set(df[col].map(str.lower))

                # Compile invalid ids, excluding "None" (lower cased).
                invalid_ids = ids - nids - {"none"}

                # Configure error properties.
                if len(invalid_ids):
                    for invalid_id in invalid_ids:
                        errors[1].append(f"{id_table}.{col} '{invalid_id}' is not present in {nid_table}.nid.")

        return errors

    def out_of_scope(self, name: str, junction: str = "junction") -> Dict[int, list]:
        """
        Validates the containment of geometries within the associated provincial / territorial boundaries.
        NatProvTer junctions are used to infer boundaries, therefore, a record will only be flagged if one of it's
        endpoints lies outside of the provincial / territorial boundaries.

        :param str name: NRN dataset name.
        :param str junction: NRN dataset name for NRN junction.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        # Validation: ensure geometries are completely within the associated provincial / territorial boundary.
        errors = defaultdict(list)
        series = self.dframes[name]["geometry"]
        junction = self.dframes[junction]

        # Compile out-of-scope junctions (natprovter).
        natprovter = set(chain.from_iterable(junction.loc[junction["junctype"] == "NatProvTer", "geometry"].map(
            lambda g: attrgetter("coords")(g))))

        # Compile series points.
        if series.iloc[0].geom_type == "LineString":
            series_pts = series.map(lambda g: set(itemgetter(0, -1)(attrgetter("coords")(g))))
        else:
            series_pts = series.map(lambda g: {itemgetter(0)(attrgetter("coords")(g))})

        # Flag series points within the set of natprovter points.
        mask = series_pts.map(lambda pts: len(pts.intersection(natprovter)) > 0)

        # Compile uuids of flagged records.
        errors[1] = series.loc[mask].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def point_proximity(self, name: str) -> Dict[int, list]:
        """
        Validates the proximity of points.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        # Validation: ensure points are >= 5 meters from each other.
        errors = defaultdict(list)
        prox_limit = 5
        series = self.dframes_m[name]["geometry"]

        # Compile coordinates (used multiple times)
        pts = series.map(lambda g: itemgetter(0)(attrgetter("coords")(g)))

        # Generate kdtree.
        tree = cKDTree(pts.to_list())

        # Compile indexes of points with other points within 5 meters distance. Only keep results with > 1 match.
        proxi_idx_all = pts.map(lambda pt: set(chain(*tree.query_ball_point([pt], r=prox_limit))))
        proxi_idx_all = proxi_idx_all.loc[proxi_idx_all.map(len) > 1]

        # Compile and filter coincident index from each set of indexes for each point, keep non-empty results.
        proxi_idx_exclude = pd.Series(range(len(pts)), index=pts.index).map(lambda index: {index})
        proxi_idx_keep = proxi_idx_all - proxi_idx_exclude.loc[proxi_idx_all.index]
        proxi_idx_keep = proxi_idx_keep.map(tuple).explode()

        # Compile uuids associated with each index.
        pts_idx_uuid_lookup = {index: uid for index, uid in enumerate(pts.index)}
        results = proxi_idx_keep.map(lambda idx: itemgetter(idx)(pts_idx_uuid_lookup))

        # Reduce duplicated result pairs.
        results = pd.Series(tuple(set(map(lambda vals: tuple(sorted(vals)), results.items()))))

        # Compile error properties: calculate min distance measurement between source and target geometries.
        distances = results.map(lambda idxs: euclidean(*itemgetter(*idxs)(pts))).round(2)

        # Compile error properties: compile and sort final results.
        results = pd.DataFrame({"target": results.map(itemgetter(1)).values, "distance": distances.values},
                               index=results.map(itemgetter(0)).values).sort_values(by="distance", ascending=True)

        # Compile error properties: store results.
        for vals in results.itertuples(index=True):
            source, target, distance = attrgetter("Index", "target", "distance")(vals)
            errors[1].append(f"uuids: '{source}', '{target}' are too close: {distance} meters.")

        return errors

    def roadclass_rtnumber_relationship(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to roadclass and rtnumber1 fields.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Filter dataframe to only required fields.
        df_filtered = df[["roadclass", "rtnumber1"]]

        # Apply validations and compile uuids of flagged records.

        # Validation: ensure rtnumber1 is not the default value or "None" when roadclass = "Expressway / Highway" or
        # "Freeway".
        default = self.defaults_all[name]["rtnumber1"]
        errors[1] = df_filtered.loc[
            df_filtered["roadclass"].isin({"Expressway / Highway", "Freeway"}) &
            df_filtered["rtnumber1"].map(lambda rtnumber1: rtnumber1 in {default, "None"})].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def route_contiguity(self, roadseg: str = "roadseg", ferryseg: Union[None, str] = None) -> Dict[int, list]:
        """
        Applies a set of validations to route attributes (rows represent field groups):
            rtename1en, rtename2en, rtename3en, rtename4en,
            rtename1fr, rtename2fr, rtename3fr, rtename4fr,
            rtnumber1, rtnumber2, rtnumber3, rtnumber4, rtnumber5.

        :param str roadseg: NRN dataset name for NRN roadseg.
        :param Union[None, str] ferryseg: NRN dataset name for NRN ferryseg.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)

        # Define field groups.
        field_groups = [["rtename1en", "rtename2en", "rtename3en", "rtename4en"],
                        ["rtename1fr", "rtename2fr", "rtename3fr", "rtename4fr"],
                        ["rtnumber1", "rtnumber2", "rtnumber3", "rtnumber4", "rtnumber5"]]

        # Filter dataframes to only required fields, concatenate resulting dataframes.
        keep_fields = list(chain.from_iterable([*field_groups, ["geometry"]]))
        if ferryseg is not None:
            df = gpd.GeoDataFrame(pd.concat([self.dframes[ferryseg][keep_fields].copy(deep=True),
                                             self.dframes[roadseg][keep_fields].copy(deep=True)],
                                            ignore_index=True, sort=False))
        else:
            df = self.dframes[roadseg][keep_fields].copy(deep=True)

        # Validation: ensure route has contiguous geometry.
        for field_group in field_groups:

            logger.info(f"Validating routes in field group: {', '.join(map(str, field_group))}.")

            # Filter dataframe to records with >= 1 non-default values across the field group, keep only required
            # fields.
            default = self.defaults_all[roadseg][field_group[0]]
            df_filtered = df.loc[(df[field_group].values != default).any(axis=1), [*field_group, "geometry"]]

            # Compile route names, excluding default value and "None".
            route_names = set(np.unique(df_filtered[field_group].values)) - {default, "None"}

            # Iterate route names.
            route_count = len(route_names)
            for index, route_name in enumerate(sorted(route_names)):

                logger.info(f"Validating route {index + 1} of {route_count}: \"{route_name}\".")

                # Subset dataframe to those records with route name in at least one field.
                route_df = df_filtered.loc[(df_filtered[field_group].values == route_name).any(axis=1)]

                # Only process duplicated route names.
                if len(route_df) > 1:

                    # Load dataframe as networkx graph.
                    route_graph = helpers.gdf_to_nx(route_df, keep_attributes=False)

                    # Validate contiguity (networkx connectivity).
                    if not nx.is_connected(route_graph):

                        # Identify deadends (locations of discontiguity).
                        deadends = [coords for coords, degree in route_graph.degree() if degree == 1]
                        deadends = "\n".join(map(lambda deadend: f"{deadend[0]}, {deadend[1]}", deadends))

                        # Compile error properties.
                        errors[1].append(f"Discontiguous route: '{route_name}', based on attribute fields: "
                                         f"{', '.join(field_group)}."
                                         f"\nCoordinates of discontiguity:\n{deadends}\n")

        return errors

    def self_intersecting_elements(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to self-intersecting road elements.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]
        default = self.defaults_all[name]["nid"]

        # Validation: ensure roadclass is in ("Expressway / Highway", "Freeway", "Ramp", "Rapid Transit",
        #             "Service Lane") for all road elements which a) self-intersect and b) touch another road segment
        #             where roadclass is in this set.

        flag_nids = list()
        valid = {"Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane"}

        # Compile coords of road segments where roadclass is in the validation list.
        valid_coords = set(chain(
            *[itemgetter(0, -1)(geom.coords) for geom in df.loc[df["roadclass"].isin(valid), "geometry"].values]))

        # Single-segment road elements:

        # Retrieve single-segment self-intersections.
        # Function call intended to avoid duplicating logic in this current function.
        segments_single = self.self_intersecting_structures(df, return_segments_only=True)

        if not segments_single.empty:

            # Compile nids of road segments with coords in the validation coords list.
            flagged = segments_single["geometry"].map(lambda g: g.coords[0] in valid_coords)
            flag_nids.extend(segments_single.loc[flagged, "nid"].values)

        # Multi-segment road elements:

        # Compile multi-segment road elements (via non-unique nids).
        # Filter to nids with invalid roadclass.
        segments_multi = df.loc[(df["nid"].duplicated(keep=False)) &
                                (~df["roadclass"].isin(valid)) & (df["nid"] != default)]

        if not segments_multi.empty:

            logger.info("Validating multi-segment road elements.")

            # Compile nids of road segments with coords in the validation coords list.
            flagged_nids = segments_multi.loc[segments_multi["geometry"].map(
                lambda g: len(set(itemgetter(0, -1)(g.coords)).intersection(valid_coords)) > 0), "nid"].unique()

            if len(flagged_nids):

                # Compile dataframe records with a flagged nid.
                flagged_df = df.loc[df["nid"].isin(flagged_nids)]

                # Group geometries by nid.
                grouped_segments = helpers.groupby_to_list(flagged_df, "nid", "geometry")

                # Dissolve road segments.
                elements = grouped_segments.map(shapely.ops.linemerge)

                # Identify self-intersections and store nids.
                vals = elements.loc[elements.map(lambda element: element.is_ring or not element.is_simple)].values
                flag_nids.extend(vals)

        # Compile uuids of road segments with flagged nid and invalid roadclass.
        errors[1] = df.loc[(df["nid"].isin(flag_nids)) & (~df["roadclass"].isin(valid))].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def self_intersecting_structures(self, name: Union[gpd.GeoDataFrame, str], return_segments_only: bool = False) -> \
            Union[Dict[int, list], gpd.GeoDataFrame]:
        """
        Applies a set of validations to self-intersecting road structures.

        :param Union[gpd.GeoDataFrame, str] name: GeoDataFrame or NRN dataset name. This allows this function to be
            called by other validations.
        :param bool return_segments_only: return flagged GeoDataFrame rather than validation error messages, default
            False.
        :return Union[Dict[int, list], gpd.GeoDataFrame]: dictionary of validation codes and associated lists of error
            messages or flagged GeoDataFrame.
        """

        errors = defaultdict(list)
        flag_segments = pd.DataFrame()
        df = self.dframes[name] if isinstance(name, str) else name.copy(deep=True)
        default = self.defaults_all["roadseg"]["nid"]

        # Identify self-intersections formed by single-segment road elements (i.e. where nid is unique).

        # Compile single-segment road elements (via unique nids).
        segments = df.loc[(~df["nid"].duplicated(keep=False)) & (df["nid"] != default)]

        if not segments.empty:

            logger.info("Validating single-segment road elements.")

            # Identify self-intersections (start coord == end coord).
            flag_segments = segments.loc[segments["geometry"].map(lambda g: g.is_ring or not g.is_simple)]

            # Validation: for self-intersecting road segments, ensure structtype != "None".
            errors[1] = flag_segments.loc[flag_segments["structtype"] == "None"].index.values

        if return_segments_only:
            return flag_segments

        else:

            # Compile error properties.
            for code, vals in errors.items():
                if len(vals):
                    errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

            return errors

    def speed(self, name: str) -> Dict[int, list]:
        """
        Applies a set of validations to speed field.

        :param str name: NRN dataset name.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        df = self.dframes[name]

        # Subset dataframe to non-default values, keep only required fields.
        default = self.defaults_all[name]["speed"]
        s_filtered = df.loc[df["speed"] != default, "speed"]

        if len(s_filtered):

            # Validation 1: ensure 5 <= speed <= 120.
            # Compile uuids of flagged records.
            errors[1] = s_filtered.loc[~s_filtered.map(lambda speed: 5 <= int(speed) <= 120)].index.values

            # Validation 2: ensure speed is a multiple of 5.
            errors[2] = s_filtered.loc[s_filtered.map(lambda speed: int(speed) % 5 != 0)].index.values

        # Compile error properties.
        for code, vals in errors.items():
            if len(vals):
                errors[code] = list(map(lambda val: f"uuid: '{val}'", vals))

        return errors

    def structure_attributes(self, roadseg: str = "roadseg", junction: str = "junction") -> Dict[int, list]:
        """
        Validates the structid and structtype attributes of road segments.

        :param str roadseg: NRN dataset name for NRN roadseg.
        :param str junction: NRN dataset name for NRN junction.
        :return Dict[int, list]: dictionary of validation codes and associated lists of error messages.
        """

        errors = defaultdict(list)
        defaults = self.defaults_all[roadseg]
        roadseg = self.dframes[roadseg]
        junction = self.dframes[junction]

        # Filter dataframes to only required fields.
        junction = junction.loc[junction["junctype"] == "Dead End", "geometry"]
        roadseg = roadseg[["uuid", "structid", "structtype", "geometry"]]

        # Validation 1: ensure dead end road segments have structtype = "None" or the default field value.

        # Compile dead end coordinates.
        deadend_coords = set(chain(junction.map(lambda pt: itemgetter(0)(attrgetter("coords")(pt)))))

        # Compile road segments with potentially invalid structtype.
        roadseg_invalid = roadseg.loc[~roadseg["structtype"].isin({"None", defaults["structtype"]}), "geometry"]

        # Compile truly invalid road segments.
        roadseg_invalid = roadseg_invalid.loc[roadseg_invalid.map(
            lambda g: any(coords in deadend_coords for coords in attrgetter("coords")(g)))]

        # Compile uuids of flagged records, compile error properties.
        if len(roadseg_invalid):
            errors[1] = list(map(lambda val: f"uuid: '{val}'", roadseg_invalid.index.values))

        # Validation 2: ensure structid is contiguous.

        # Compile records with duplicated structids, excluding "None" and the default field value.
        structids_df = roadseg.loc[(~roadseg["structid"].isin({"None", defaults["structid"]})) &
                                   (roadseg["structid"].duplicated(keep=False))]

        if len(structids_df):

            # Group records by structid.
            structures = helpers.groupby_to_list(structids_df, "structid", "geometry")

            # Load structure geometries as networkx graphs.
            structure_graphs = structures.map(
                lambda geoms: helpers.gdf_to_nx(gpd.GeoDataFrame(geometry=geoms), keep_attributes=False))

            # Validate contiguity (networkx connectivity).
            structures_invalid = structure_graphs.loc[~structure_graphs.map(nx.is_connected)]

            if len(structures_invalid):

                # Identify deadends (locations of discontiguity).
                results = structures_invalid.map(lambda graph: [pt for pt, degree in graph.degree() if degree == 1])

                # Compile error properties.
                for structid, deadends in results.iteritems():
                    deadends = "\n".join(map(lambda deadend: f"{deadend[0]}, {deadend[1]}", deadends))

                    errors[2].append(f"Discontiguous structure structid: '{structid}'."
                                     f"\nCoordinates of discontiguity:\n{deadends}\n.")

        # Validation 3: ensure a single, non-default structid is applied to all contiguous road segments with the same
        #               structtype.
        # Validation 4: ensure road segments with different structtypes, excluding "None" and the default field value,
        #               are not contiguous.

        # Compile road segments with valid structtype.
        segments = roadseg.loc[~roadseg["structtype"].isin({"None", defaults["structtype"]})]

        # Convert dataframe to networkx graph.
        segments_graph = helpers.gdf_to_nx(segments, keep_attributes=True, endpoints_only=False)

        # Configure subgraphs.
        sub_g = pd.Series(list(map(segments_graph.subgraph, nx.connected_components(segments_graph))))

        # Validation 3.
        default = defaults["structid"]
        structids = sub_g.map(lambda graph: set(nx.get_edge_attributes(graph, "structid").values()))
        structids_invalid = structids.loc[structids.map(lambda vals: (len(vals) > 1) or (default in vals))]
        if len(structids_invalid):

            # Compile uuids of invalid structure.
            uuids_invalid = sub_g.loc[structids_invalid.index].map(
                lambda graph: set(nx.get_edge_attributes(graph, "uuid").values()))

            # Compile error properties.
            for index, row in pd.DataFrame({"uuids": uuids_invalid, "structids": structids_invalid}).iterrows():
                uuids = ", ".join(map(lambda val: f"'{val}'", row[0]))
                structids = ", ".join(map(lambda val: f"'{val}'", row[1]))
                errors[3].append(f"Structure formed by uuids: {uuids} contains multiple structids: {structids}.")

        # Validation 4.
        structtypes = sub_g.map(lambda graph: set(nx.get_edge_attributes(graph, "structtype").values()))
        structtypes_invalid = structtypes.loc[structtypes.map(len) > 1]
        if len(structtypes_invalid):

            # Compile uuids of invalid structure.
            uuids_invalid = sub_g.loc[structtypes_invalid.index].map(
                lambda graph: set(nx.get_edge_attributes(graph, "uuid").values()))

            # Compile error properties.
            for index, row in pd.DataFrame({"uuids": uuids_invalid, "structtypes": structtypes_invalid}).iterrows():
                uuids = ", ".join(map(lambda val: f"'{val}'", row[0]))
                structtypes = ", ".join(map(lambda val: f"'{val}'", row[1]))
                errors[4].append(f"Structure formed by uuids: {uuids} contains multiple structtypes: {structtypes}.")

        return errors

    def execute(self) -> None:
        """Orchestrates the execution of validation functions and compiles the resulting errors."""

        try:

            # Iterate validation definitions.
            for func, params in self.validations.items():
                for dataset in params["datasets"]:

                    # Continue with single dataset or compile all if non-iterative.
                    datasets = (dataset,) if params["iterate"] else (*params["datasets"],)

                    logger.info(f"Applying validation \"{func.__name__}\" to dataset(s): {', '.join(datasets)}.")

                    # Validate dataset availability.
                    missing = set(datasets) - set(self.dframes)
                    if missing:
                        logger.warning(f"Skipping validation due to missing dataset(s): {', '.join(missing)}.")
                        if params["iterate"]:
                            continue
                        else:
                            break

                    # Execute validation.
                    results = func(*datasets)

                    # Generate error heading and store results.
                    for code, errors in results.items():
                        if len(errors):
                            heading = f"E{params['code']:03}{code:02} for dataset(s): {', '.join(datasets)}"
                            self.errors[heading] = errors

        except (KeyError, SyntaxError, ValueError) as e:
            logger.exception("Unable to apply validation.")
            logger.exception(e)
            sys.exit(1)
