import click
import geopandas as gpd
import logging
import pandas as pd
import string
import sys
import uuid
from itertools import compress
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge
from typing import Tuple

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

# Create logger for change logs.
logger_change_logs = logging.getLogger("change_logs")
logger_change_logs.setLevel(logging.INFO)


class Confirm:
    """Defines an NRN process."""

    def __init__(self, source: str, remove: bool = False) -> None:
        """
        Initializes an NRN process.

        :param str source: abbreviation for the source province / territory.
        :param bool remove: removes pre-existing change logs within the data/processed directory for the specified
            source, default False.
        """

        self.source = source.lower()
        self.remove = remove

        # Configure data paths.
        self.src = filepath.parents[2] / f"data/interim/{self.source}.gpkg"
        self.dst = filepath.parents[2] / f"data/processed/{self.source}/{self.source}_change_logs"

        # Validate source path.
        if not self.src.exists():
            logger.exception(f"Source not found: \"{self.src}\".")
            sys.exit(1)

        # Validate and conditionally clear output namespace.
        if self.dst.exists():
            logger.warning("Output namespace already occupied.")

            if self.remove:
                logger.warning("Parameter remove=True: Removing directory.")
                helpers.rm_tree(self.dst)

            else:
                logger.exception("Parameter remove=False: Unable to proceed while output namespace is occupied. Set "
                                 "remove=True (-r) or manually clear the output namespace.")
                sys.exit(1)

        # Define match fields (fields used for grouping records in current dataset / linking to old dataset)
        # Note: roadseg requires a match field, the remaining entries are optional.
        self.match_fields = {
            "blkpassage": "blkpassty",
            "junction": "junctype",
            "roadseg": "r_stname_c",
            "tollpoint": "tollpttype"
        }

        # Load default field values.
        self.defaults = helpers.compile_default_values()

        # Load data - current and previous vintage.
        self.dframes = helpers.load_gpkg(self.src,
                                         layers=["blkpassage", "ferryseg", "junction", "roadseg", "tollpoint"])
        self.dframes_old = helpers.load_gpkg(self.src.parent / f"{self.source}_old.gpkg", find=True,
                                             layers=["blkpassage", "ferryseg", "junction", "roadseg", "tollpoint"])

        # Define change logs dictionary.
        self.change_logs = {
            table: {change: set() for change in ("added", "retired", "modified", "confirmed")} for table in self.dframes
        }

    def __call__(self) -> None:
        """Executes an NRN process."""

        self.gen_nids()
        self.gen_structids()
        self.update_nid_linkages()
        self.export_nid_change_logs()
        helpers.export(self.dframes, self.src)

    def export_nid_change_logs(self) -> None:
        """Exports nid change classifications as log files."""

        logger.info(f"Writing nid change logs to: \"{self.dst}\".")

        # Create change logs directory.
        Path(self.dst).mkdir(parents=True, exist_ok=True)

        # Iterate tables and nid classification types.
        for table in self.change_logs:
            for classification, log in self.change_logs[table].items():

                # Configure log path.
                log_path = self.dst / f"{self.source}_{table}_{classification}.log"

                # Drop pre-existing File Handler.
                for f_handler in logger_change_logs.handlers:
                    logger_change_logs.removeHandler(f_handler)

                # Add File Handler with new log path.
                f_handler = logging.FileHandler(log_path)
                f_handler.setLevel(logging.INFO)
                f_handler.setFormatter(logger.handlers[0].formatter)
                logger_change_logs.addHandler(f_handler)

                # Write log.
                logger_change_logs.info(log)

    def gen_nids(self) -> None:
        """
        Generates NID values for each dataset. Additionally recovers NIDs from the previous version, where possible.
        """

        logger.info("Generating NIDs.")

        # Iterate datasets.
        valid_dframes = {table: df.copy(deep=True) for table, df in self.dframes.items() if "geometry" in df.columns}
        for table, df in valid_dframes.items():

            logger.info(f"Generating NIDs for dataset: {table}.")

            # Fetch old dataset, match field, and defaults.
            df_old = self.dframes_old[table].loc[self.validate_ids(self.dframes_old[table]["nid"])].copy(deep=True)
            match_field = self.match_fields[table] if table in self.match_fields else None
            default = self.defaults[table]["nid"]

            # Copy original (non-dissolved) data.
            df_orig = df.copy(deep=True)

            # Modify geometries prior to standard nid generation process.
            if table == "roadseg":

                # Compile junctions as splitting points.
                junctions = self.dframes["junction"].loc[self.dframes["junction"]["junctype"] != "Dead End", "geometry"]
                junctions = gpd.GeoSeries(junctions.unique(), crs=junctions.crs)

                # Dissolve geometries, grouped by match field, and explode multi-part results.
                df_merge = helpers.groupby_to_list(df, group_field=match_field, list_field="geometry")\
                    .map(linemerge).explode()
                df_merge = gpd.GeoDataFrame({match_field: df_merge.index}, geometry=df_merge.values, crs=df.crs)

                # Compile junctions, as coordinates, contained within each dissolved geometry.
                junctions_idx_geom_lookup = dict(junctions.map(lambda pt: itemgetter(0)(attrgetter("coords")(pt))))
                df_merge["junction_idxs"] = df_merge["geometry"].map(
                    lambda g: junctions.sindex.query(g, predicate="contains")).map(tuple)
                flag_split = df_merge["junction_idxs"].map(len) > 0

                df_merge["junctions"] = None
                df_merge.loc[flag_split, "junctions"] = df_merge.loc[flag_split, "junction_idxs"]\
                    .map(lambda idxs: itemgetter(*idxs)(junctions_idx_geom_lookup))\
                    .map(lambda pts: (pts,) if not isinstance(pts[0], tuple) else pts)

                # Split geometries on junctions; explode multi-part results.
                # Overwrite df variable with results to feed into generic process flow.
                df_merge["split"] = None
                df_merge.loc[flag_split, "split"] = pd.Series(zip(df_merge.loc[flag_split, "geometry"],
                                                                  df_merge.loc[flag_split, "junctions"])).values
                df_merge.loc[flag_split, "geometry"] = df_merge.loc[flag_split, "split"].map(
                    lambda geoms: self.split_line(*geoms))
                df = df_merge.explode(ignore_index=True)[[match_field, "geometry"]]

                # Create dissolved geometries, grouped by nid, for old dataset.
                # Overwrite df variable with results to feed into generic process flow.
                old_nid_match_field_lookup = dict(zip(df_old["nid"], df_old[match_field]))
                df_merge_old = helpers.groupby_to_list(df_old, group_field="nid", list_field="geometry").map(linemerge)
                df_old = gpd.GeoDataFrame(
                    {"nid": df_merge_old.index, match_field: df_merge_old.index.map(old_nid_match_field_lookup)},
                    geometry=df_merge_old.values, crs=df_old.crs
                )

                # Filter out multi-part geometries from old dataset.
                df_old = df_old.loc[df_old.geom_type == "LineString"].copy(deep=True)

            # Generate and classify nids.

            # Compile geometry as wkb.
            df_wkb = df["geometry"].to_wkb(hex=False)
            df_old_wkb = df_old["geometry"].to_wkb(hex=False)

            # Generate wkb-nid and nid-match_field lookup dicts from old dataset.
            wkb_nid_lookup = dict(zip(df_old_wkb, df_old["nid"]))
            nid_match_lookup = dict(zip(df_old["nid"], df_old[match_field])) if match_field else dict()
            nid_match_lookup[default] = default

            # Recover nids from wkb-nid lookup.
            df["nid"] = df_wkb.map(wkb_nid_lookup).fillna(default)
            self.change_logs[table]["confirmed"] = set(df.loc[df["nid"] != default, "nid"])

            # Identify modified records based on match field.
            if match_field:
                flag_modified = (df["nid"] != default) & (df[match_field] != df["nid"].map(nid_match_lookup))

                self.change_logs[table]["modified"] = set(df.loc[flag_modified, "nid"])
                self.change_logs[table]["confirmed"] = \
                    self.change_logs[table]["confirmed"] - set(df.loc[flag_modified, "nid"])

            # Assign a new nid to all required records.
            flag_added = (df["nid"] == default)
            df.loc[flag_added, "nid"] = [uuid.uuid4().hex for _ in range(sum(flag_added))]

            self.change_logs[table]["added"] = set(df.loc[flag_added, "nid"])
            self.change_logs[table]["retired"] = set(df_old["nid"]) - set(df["nid"])

            # Link dissolved geometries to original geometries, if required.
            if table == "roadseg":

                # Compile index of dissolved geometry associated with each original geometry.
                covered_by = df_orig["geometry"].map(lambda g: df.sindex.query(g, predicate="covered_by"))

                # Identify invalid linkages (occurs for complex LineStrings).
                invalid = set(covered_by.loc[covered_by.map(len) != 1].index)
                if len(invalid):

                    # Resolve invalid linkages.
                    covered_by = self.resolve_complex_linkages(df_orig, df, covered_by, invalid)

                # Generate dissolved dataset idx-nid lookup and recover nids for non-dissolved dataset.
                idx_nid_lookup = dict(zip(range(len(df)), df["nid"]))
                covered_by = covered_by.map(itemgetter(0)).map(idx_nid_lookup)

                # Overwrite dissolved dataset with non-dissolved nid series.
                df = pd.DataFrame({"nid": covered_by.values}, index=covered_by.index)

            # Store results.
            self.dframes[table]["nid"] = df["nid"].copy(deep=True)

    def gen_structids(self) -> None:
        """
        Generates structid values for roadseg. Additionally recovers structids from the previous version, where
        possible.
        """

        logger.info("Generating structids for dataset: roadseg.")

        # Overwrite any pre-existing structid.
        self.dframes["roadseg"]["structid"] = "None"

        # Copy and filter dataframes.
        default = self.defaults["roadseg"]["structtype"]
        struct = self.dframes["roadseg"].loc[
            ~self.dframes["roadseg"]["structtype"].isin({"None", default})].copy(deep=True)
        struct_old = self.dframes_old["roadseg"].loc[
            (~self.dframes_old["roadseg"]["structtype"].isin({"None", default})) &
            (self.validate_ids(self.dframes_old["roadseg"]["structid"]))].copy(deep=True)

        if len(struct):

            default = self.defaults["roadseg"]["structid"]

            # Dissolve contiguous structures, explode multi-part results.
            struct_merge = gpd.GeoDataFrame(geometry=[linemerge(struct["geometry"].values)], crs=struct.crs)\
                .explode(ignore_index=True)

            # Dissolve contiguous structures, grouped by structid, for old dataset.
            struct_merge_old = helpers.groupby_to_list(struct_old, group_field="nid", list_field="geometry")\
                .map(linemerge)
            struct_merge_old = gpd.GeoDataFrame(
                {"structid": struct_merge_old.index}, geometry=struct_merge_old.values, crs=struct_old.crs)

            # Filter out multi-part geometries from old dataset.
            struct_merge_old = struct_merge_old.loc[struct_merge_old.geom_type == "LineString"].copy(deep=True)

            # Compile geometry as wkb.
            struct_merge_wkb = struct_merge["geometry"].to_wkb(hex=False)
            struct_merge_old_wkb = struct_merge_old["geometry"].to_wkb(hex=False)

            # Generate wkb-structid lookup from old dataset and recover structids.
            wkb_structid_lookup = dict(zip(struct_merge_old_wkb, struct_merge_old["structid"]))
            struct_merge["structid"] = struct_merge_wkb.map(wkb_structid_lookup).fillna(default)

            # Assign a new structid to all required records.
            flag_added = (struct_merge["structid"] == default)
            struct_merge.loc[flag_added, "structid"] = [uuid.uuid4().hex for _ in range(sum(flag_added))]

            # Link dissolved geometries to original geometries.

            # Compile index of dissolved geometry associated with each original geometry.
            covered_by = struct["geometry"].map(lambda g: struct_merge.sindex.query(g, predicate="covered_by"))

            # Identify invalid linkages (occurs for complex LineStrings).
            invalid = set(covered_by.loc[covered_by.map(len) != 1].index)
            if len(invalid):

                # Resolve invalid linkages.
                covered_by = self.resolve_complex_linkages(struct, struct_merge, covered_by, invalid)

            # Generate dissolved dataset idx-structid lookup and recover structids for non-dissolved dataset.
            idx_structid_lookup = dict(zip(range(len(struct_merge)), struct_merge["structid"]))
            covered_by = covered_by.map(itemgetter(0)).map(idx_structid_lookup)

            # Store results.
            self.dframes["roadseg"].loc[covered_by.index, "structid"] = covered_by.copy(deep=True)

    @staticmethod
    def resolve_complex_linkages(df: gpd.GeoDataFrame, df_dissolved: gpd.GeoDataFrame, covered_by: pd.Series,
                                 invalid_ids: set) -> pd.Series:
        """
        Resolves invalid covered_by results by identifying the indended result via intersection.
        Invalid binary predicate results is a known issue for complex geometries
        (https://github.com/shapely/shapely/issues/17).

        :param gpd.GeoDataFrame df: GeoDataFrame containing original geometries.
        :param gpd.GeoDataFrame df_dissolved: GeoDataFrame containing dissolved geometries and NIDs.
        :param pd.Series covered_by: covered_by results.
        :param set invalid_ids: identifiers (indexes) of `df` records with invalid covered_by results.
        :return pd.Series: resolved `covered_by`.
        """

        # Create subset dataframe containing invalid linkages.
        df_ = df.loc[df.index.isin(invalid_ids)].copy(deep=True)

        # Compile indexes and geometries of intersecting dissolved geometries.
        df_["intersects_idxs"] = df_["geometry"].map(lambda g: df_dissolved.sindex.query(g, predicate="intersects"))
        df_["intersects_geoms"] = df_["intersects_idxs"].map(lambda idxs: itemgetter(*idxs)(df_dissolved["geometry"]))

        # Flag dissolved geometries which overlap the base geometry (must use `intersection` instead of predicates).
        df_["overlaps_flag"] = df_[["geometry", "intersects_geoms"]].apply(lambda row: tuple(map(
            lambda geom: isinstance(row[0].intersection(geom), (LineString, MultiLineString)), row[1])), axis=1)

        # Compile index of flagged dissolved geometry.
        df_["resolved_idx"] = df_[["intersects_idxs", "overlaps_flag"]].apply(lambda row: list(compress(*row)), axis=1)

        # Update covered_by results with resolved identifiers.
        covered_by.loc[df_.index] = df_["resolved_idx"]

        return covered_by.copy(deep=True)

    @staticmethod
    def split_line(line: LineString, pts: Tuple[tuple, ...]) -> MultiLineString:
        """
        Splits a LineString on a collection of points.

        :param LineString line: LineString to be split.
        :param Tuple[tuple, ...] pts: Tuple of point coordinates used to split the input LineString.
        :return MultiLineString: MultiLineString representing the segmented input LineString.
        """

        # Compile LineString coordinates.
        line_pts = tuple(attrgetter("coords")(line))

        # Compile indexes of points along LineString, convert to ranges.
        idxs = sorted({0, *map(lambda pt: line_pts.index(pt), pts), len(line_pts) - 1})
        ranges = tuple(zip(idxs[:-1], idxs[1:]))

        # Split LineString at point indexes.
        return MultiLineString(tuple(map(lambda rng: LineString(line_pts[rng[0]: rng[1] + 1]), ranges)))

    def update_nid_linkages(self) -> None:
        """
        Updates the nid linkages of NRN roadseg:
        1) blkpassage.roadnid
        2) tollpoint.roadnid
        """

        logger.info("Updating nid linkages for table: roadseg.")

        # Check table existence.
        tables = [table for table in ("blkpassage", "tollpoint") if table in self.dframes]

        if tables:

            # Copy roadseg and reproject to meter-based crs.
            roadseg = self.dframes["roadseg"].to_crs("EPSG:3348").copy(deep=True)

            # Create roadseg idx-nid lookup dict. Add nid default to dict.
            roadseg_idx_nid_lookup = dict(zip(range(len(roadseg)), roadseg["nid"]))
            default = self.defaults["roadseg"]["nid"]
            roadseg_idx_nid_lookup[default] = default

            # Iterate dataframes, if available.
            for table in tables:

                logger.info(f"Updating nid linkages for table relationship: {table} - roadseg.")

                # Copy table dataframe and reproject to meter-based crs.
                df = self.dframes[table].to_crs("EPSG:3348").copy(deep=True)

                # Create idx-idx lookup dict for nearest features between table and roadseg.
                nearest_idx_lookup = dict(zip(*roadseg.sindex.nearest(
                    df["geometry"], return_all=False, max_distance=5, return_distance=False)))

                # Populate table roadnid based on lookup dicts.
                df["roadnid"] = range(len(df))
                df["roadnid"] = df["roadnid"].map(nearest_idx_lookup).fillna(default).map(roadseg_idx_nid_lookup)

                # Store results.
                self.dframes[table]["roadnid"] = df["roadnid"].copy(deep=True)

    @staticmethod
    def validate_ids(series: pd.Series) -> pd.Series:
        """
        Validates a Series of IDs based on the following conditions:
        1) ID must be non-null.
        2) ID must be 32 digits.
        3) ID must be hexadecimal.

        :param pd.Series series: Series.
        :return pd.Series: boolean Series.
        """

        hexdigits = set(string.hexdigits)

        # Filter records.
        flags = ~((series.isna()) |
                  (series.map(lambda val: len(str(val)) != 32)) |
                  (series.map(lambda val: not set(str(val)).issubset(hexdigits))))

        return flags


@click.command()
@click.argument("source", type=click.Choice("ab bc mb nb nl ns nt nu on pe qc sk yt".split(), False))
@click.option("--remove / --no-remove", "-r", default=False, show_default=True,
              help="Remove pre-existing change logs within the data/processed directory for the specified source.")
def main(source: str, remove: bool = False) -> None:
    """
    Executes an NRN process.

    :param str source: abbreviation for the source province / territory.
    :param bool remove: removes pre-existing change logs within the data/processed directory for the specified source,
        default False.
    """

    try:

        with helpers.Timer():
            process = Confirm(source, remove)
            process()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
