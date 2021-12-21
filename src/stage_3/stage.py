import click
import geopandas as gpd
import logging
import networkx as nx
import numpy as np
import pandas as pd
import string
import sys
import uuid
from itertools import chain, compress
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely.geometry import LineString, MultiPoint, Point
from shapely.ops import linemerge, split

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


class Stage:
    """Defines an NRN stage."""

    def __init__(self, source: str, remove: bool = False) -> None:
        """
        Initializes an NRN stage.

        :param str source: abbreviation for the source province / territory.
        :param bool remove: removes pre-existing change logs within the data/processed directory for the specified
            source, default False.
        """

        self.stage = 3
        self.source = source.lower()
        self.remove = remove

        # Configure and validate input data path.
        self.data_path = filepath.parents[2] / f"data/interim/{self.source}.gpkg"
        if not self.data_path.exists():
            logger.exception(f"Input data not found: \"{self.data_path}\".")
            sys.exit(1)

        # Configure output path.
        self.output_path = filepath.parents[2] / f"data/processed/{self.source}/{self.source}_change_logs"

        # Conditionally clear output namespace.
        if self.output_path.exists():
            logger.warning("Output namespace already occupied.")

            if self.remove:
                logger.warning("Parameter remove=True: Removing directory.")
                helpers.rm_tree(self.output_path)

            else:
                logger.exception("Parameter remove=False: Unable to proceed while output namespace is occupied. Set "
                                 "remove=True (-r) or manually clear the output namespace.")
                sys.exit(1)

        # Compile match fields (fields which must be equal across records).
        self.match_fields = ["r_stname_c"]

        # Define change logs dictionary.
        self.change_logs = dict()

        # Load default field values.
        self.defaults = helpers.compile_default_values()["roadseg"]

        # Load data - current and previous vintage.
        self.dframes = helpers.load_gpkg(self.data_path)
        self.dframes_old = helpers.load_gpkg(self.data_path.parent / f"{self.source}_old.gpkg", find=True)

    def export_change_logs(self) -> None:
        """Exports the dataset differences as logs - based on nids."""

        logger.info(f"Writing change logs to: \"{self.output_path}\".")

        # Create change logs directory.
        Path(self.output_path).mkdir(parents=True, exist_ok=True)

        # Iterate tables and change types.
        for table in self.change_logs:
            for change, log in self.change_logs[table].items():

                # Configure log path.
                log_path = self.output_path / f"{self.source}_{table}_{change}.log"

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

    def gen_and_recover_structids(self) -> None:
        """Recovers structids from the previous NRN vintage or generates new ones."""

        logger.info("Generating structids for table: roadseg.")

        # Overwrite any pre-existing structid.
        self.dframes["roadseg"]["structid"] = [uuid.uuid4().hex for _ in range(len(self.dframes["roadseg"]))]
        self.dframes["roadseg"].loc[self.dframes["roadseg"]["structtype"].isin({"None", self.defaults["structtype"]}),
                                    "structid"] = "None"
        self.roadseg.loc[self.dframes["roadseg"].index, "structid"] = self.dframes["roadseg"]["structid"]

        # Copy and filter dataframes.
        roadseg = self.dframes["roadseg"][["uuid", "structid", "structtype", "geometry"]].copy(deep=True)
        roadseg_old = self.dframes_old["roadseg"][["structid", "structtype", "geometry"]].copy(deep=True)

        # Subset dataframes to valid structures.
        # Further subset previous vintage to records with valid IDs.
        roadseg = roadseg.loc[~roadseg["structtype"].isin({"None", self.defaults["structtype"]})]
        roadseg_old = roadseg_old.loc[self.get_valid_ids(roadseg_old["structid"])]

        if len(roadseg):

            # Group contiguous structures.
            # Process: compile networkx subgraphs, assign a structid to each list of subgraph uuids.
            graph = helpers.gdf_to_nx(roadseg, keep_attributes=True, endpoints_only=True)
            subgraphs = map(graph.subgraph, nx.connected_components(graph))
            structids = dict()

            for subgraph in subgraphs:
                structids[uuid.uuid4().hex] = list(set(nx.get_edge_attributes(subgraph, "uuid").values()))

            # Explode uuid groups and invert series-index such that the uuid is the index.
            structids = pd.Series(structids).explode()
            structids = pd.Series(structids.index.values, index=structids)

            # Assign structids to dataframe.
            roadseg.loc[structids.index, "structid"] = structids

            # Recovery old structids.
            logger.info("Recovering old structids for table: roadseg.")

            # Group by structid.
            roadseg_grouped = helpers.groupby_to_list(roadseg, "structid", "geometry")
            roadseg_old_grouped = helpers.groupby_to_list(roadseg_old, "structid", "geometry")

            # Dissolve grouped geometries.
            roadseg_grouped = roadseg_grouped.map(lambda geoms: geoms[0] if len(geoms) == 1 else linemerge(geoms))
            roadseg_old_grouped = roadseg_old_grouped.map(
                lambda geoms: geoms[0] if len(geoms) == 1 else linemerge(geoms))

            # Convert series to geodataframes.
            # Restore structid index as column.
            roadseg_grouped = gpd.GeoDataFrame({"structid": roadseg_grouped.index}, geometry=roadseg_grouped.values)
            roadseg_old_grouped = gpd.GeoDataFrame({"structid": roadseg_old_grouped.index},
                                                   geometry=roadseg_old_grouped.values)

            # Merge current and old dataframes on geometry.
            merge = pd.merge(roadseg_old_grouped, roadseg_grouped, how="outer", on="geometry", suffixes=("_old", ""),
                             indicator=True)

            # Recover old structids.
            # Process: Filter merged dataframes to only those with matches on both, create a lookup dict between the new
            # and old structids.
            recovery = merge.loc[merge["_merge"] == "both"].drop_duplicates(subset="structid", keep="first")
            recovery.index = recovery["structid"]

            # Filter invalid structids from old data.
            recovery = recovery.loc[self.get_valid_ids(recovery["structid_old"])]

            # Recover old structids.
            recovery_lookup = recovery["structid_old"].to_dict()

            if len(recovery_lookup):
                flag = roadseg["structid"].isin(recovery_lookup)
                roadseg.loc[flag, "structid"] = roadseg.loc[flag, "structid"].map(recovery_lookup)

            # Store results.
            self.roadseg.loc[roadseg.index, "structid"] = roadseg["structid"].copy(deep=True)
            self.dframes["roadseg"].loc[self.roadseg.index, "structid"] = self.roadseg["structid"].copy(deep=True)

    def get_valid_ids(self, series: pd.Series) -> pd.Series:
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

    def recover_and_classify_nids(self) -> None:
        """
        For all spatial datasets, excluding NRN roadseg:
        1) Recovers nids from the previous NRN vintage or generates new ones.
        2) Generates 4 nid classification log files: added, retired, modified, confirmed.
        """

        # Iterate datasets.
        for table in ("blkpassage", "ferryseg", "junction", "tollpoint"):

            # Check dataset existence.
            if table in self.dframes:

                logger.info(f"Generating nids for table: {table}.")

                # Assign nids to current vintage.
                self.dframes[table]["nid"] = [uuid.uuid4().hex for _ in range(len(self.dframes[table]))]

                # Recover old nids, if old dataset is available.
                # Classify nids.
                if table in self.dframes_old:

                    logger.info(f"Recovering old nids and classifying all nids for table: {table}.")

                    # Copy and filter dataframes.
                    df = self.dframes[table][["nid", "uuid", "geometry"]].copy(deep=True)
                    df_old = self.dframes_old[table][["nid", "geometry"]].copy(deep=True)

                    # Merge current and old dataframes on geometry.
                    merge = df.merge(df_old, how="outer", on="geometry", suffixes=("", "_old"), indicator=True)\
                        .copy(deep=True)

                    # Classify nid groups as: added, retired, modified, confirmed.
                    classified_nids = {
                        "added": merge.loc[merge["_merge"] == "right_only", "nid"].to_list(),
                        "retired": merge.loc[merge["_merge"] == "left_only", "nid_old"].to_list(),
                        "modified": list(),
                        "confirmed": merge.loc[merge["_merge"] == "both"]
                    }

                    # Recover old nids for confirmed and modified nid groups.
                    # Process: Filter merged dataframes to only those with matches on both, create a lookup dict between
                    # the new and old nids.
                    recovery = merge.loc[merge["_merge"] == "both"].drop_duplicates(subset="nid", keep="first")\
                        .copy(deep=True)
                    recovery.index = recovery["nid"]

                    # Filter invalid nids from old data.
                    recovery = recovery.loc[self.get_valid_ids(recovery["nid_old"])]

                    # Recover old nids.
                    recovery_lookup = recovery["nid_old"].to_dict()

                    if len(recovery_lookup):
                        flag = df["nid"].isin(recovery_lookup)
                        df.loc[flag, "nid"] = df.loc[flag, "nid"].map(recovery_lookup)

                    # Store results.
                    self.dframes[table].loc[df.index, "nid"] = df["nid"].copy(deep=True)

                    # Update confirmed nid classification.
                    classified_nids["confirmed"] = classified_nids["confirmed"]["nid"].to_list()

                # Classify nids.
                else:

                    logger.info(f"Classifying all nids for table: {table}. No old nid recovery required.")

                    classified_nids = {
                        "added": self.dframes[table]["nid"].to_list(),
                        "retired": list(),
                        "modified": list(),
                        "confirmed": list()
                    }

                # Store nid classifications as change logs.
                self.change_logs[table] = {
                    change: "\n".join(map(str, ["Records listed by nid:", *nids])) if len(nids) else "No records." for
                    change, nids in classified_nids.items()
                }

    def roadseg_gen_full(self) -> None:
        """
        Generates the full representation of NRN roadseg with all required fields for NID recovery for both the current
        and previous vintage.
        """

        logger.info("Generating full roadseg representation.")

        # Copy and filter dataframe - current vintage.
        self.roadseg = self.dframes["roadseg"][["uuid", "nid", "geometry", *self.match_fields]].copy(deep=True)
        self.roadseg.index = self.roadseg["uuid"]

        # Copy and filter dataframe - previous vintage.
        self.roadseg_old = self.dframes_old["roadseg"][["nid", "geometry", *self.match_fields]].copy(deep=True)

    def roadseg_gen_nids(self) -> None:
        """Groups NRN roadseg records and assigns nid values."""

        logger.info("Generating nids for table: roadseg.")

        # Overwrite any pre-existing nid.
        self.dframes["roadseg"]["nid"] = [uuid.uuid4().hex for _ in range(len(self.dframes["roadseg"]))]
        self.roadseg.loc[self.dframes["roadseg"].index, "nid"] = self.dframes["roadseg"]["nid"]

        # Copy and filter dataframes.
        roadseg = self.roadseg[[*self.match_fields, "uuid", "nid", "geometry"]].copy(deep=True)
        junction = self.dframes["junction"][["uuid", "geometry"]].copy(deep=True)

        # Subset dataframes to where at least one match field is not equal to the default value nor "None".
        default = self.defaults[self.match_fields[0]]
        roadseg = roadseg.loc[~(
                (roadseg[self.match_fields].eq(roadseg[self.match_fields].iloc[:, 0], axis=0).all(axis=1)) &
                (roadseg[self.match_fields[0]].isin(["None", default])))]

        # Group uuids and geometry by match fields.
        # To reduce processing, only duplicated records are grouped.
        dups = roadseg.loc[roadseg[self.match_fields].duplicated(keep=False)]
        dups_geom_lookup = dups["geometry"].to_dict()
        grouped = dups.groupby(self.match_fields)["uuid"].agg(list)

        # Split groups which exceed the processing threshold.
        # Note: The threshold and new size are arbitrary. Change them if required.
        threshold = 10000
        new_size = 1000
        invalid_groups = grouped.loc[grouped.map(len) >= threshold].copy(deep=True)
        grouped.drop(invalid_groups.index, inplace=True)
        for invalid_group in invalid_groups:
            grouped = grouped.append(pd.Series([invalid_group[start_idx * new_size: (start_idx * new_size) + new_size]
                                                for start_idx in range(int(len(invalid_group) / new_size) + 1)]))

        # Compile associated geometries for each uuid group as a dataframe.
        grouped = pd.DataFrame({"uuid": grouped.values,
                                "geometry": grouped.map(lambda uuids: itemgetter(*uuids)(dups_geom_lookup)).values},
                               index=range(len(grouped)))

        # Dissolve geometries.
        grouped["geometry"] = grouped["geometry"].map(linemerge)

        # Concatenate non-grouped groups (single uuid groups) to groups.
        non_grouped = roadseg.loc[~roadseg[self.match_fields].duplicated(keep=False), ["uuid", "geometry"]]
        non_grouped["uuid"] = non_grouped["uuid"].map(lambda uid: [uid])
        grouped = pd.concat([grouped, non_grouped], axis=0, ignore_index=True, sort=False)

        # Split multilinestrings into multiple linestring records.
        # Process: query and explode multilinestring records, then concatenate to linestring records.
        grouped_single = grouped.loc[~grouped["geometry"].map(lambda geom: geom.type == "MultiLineString")]
        grouped_multi = grouped.loc[grouped["geometry"].map(lambda geom: geom.type) == "MultiLineString"]

        grouped_multi_exploded = grouped_multi.explode("geometry")
        grouped = pd.concat([grouped_single, grouped_multi_exploded], axis=0, ignore_index=False, sort=False)

        # Compile coincident junctions to each linestring point, excluding endpoints.
        junction_pts = set(chain.from_iterable(junction["geometry"].map(attrgetter("coords"))))
        grouped["junction"] = grouped["geometry"].map(lambda geom: set(list(geom.coords)[1: -1]))
        grouped["junction"] = grouped["junction"].map(lambda coords: list(coords.intersection(junction_pts)))

        # Separate groups with and without coincident junctions.
        grouped_no_junction = grouped.loc[~grouped["junction"].map(lambda indexes: len(indexes) > 0)].copy(deep=True)
        grouped_junction = grouped.loc[grouped["junction"].map(lambda indexes: len(indexes) > 0)].copy(deep=True)

        # Convert coords to shapely points.
        grouped_junction["junction"] = grouped_junction["junction"].map(
            lambda pts: Point(pts) if len(pts) == 1 else MultiPoint(pts))

        # Split linestrings on junctions, only for groups with coincident junctions.
        grouped_junction["geometry"] = np.vectorize(lambda line, pts: split(line, pts), otypes=[LineString])(
            grouped_junction["geometry"], grouped_junction["junction"])

        # Split multilinestrings into multiple linestring records, concatenate all split records to non-split records.
        # Process: reset indexes, explode multilinestring records from split results, then concatenate all split and
        # non-split results.
        grouped_junction.reset_index(drop=True, inplace=True)
        grouped_no_junction.reset_index(drop=True, inplace=True)

        grouped_junction_exploded = grouped_junction.explode("geometry")
        grouped = pd.concat([grouped_no_junction, grouped_junction_exploded], axis=0, ignore_index=True, sort=False)

        # Every row now represents an nid group.
        # Attributes:
        # 1) geometry: represents the dissolved geometry of the now-reduced group.
        # 2) uuids: the original attribute grouping of uuids.
        # The uuid group now needs to be reduced to match the now-reduced geometry.
        grouped = pd.DataFrame({"uuids": grouped["uuid"], "geometry": grouped["geometry"].map(lambda g: set(g.coords))})

        # Retrieve roadseg geometries for associated uuids.
        roadseg_geometry = roadseg["geometry"].map(lambda geom: set(itemgetter(0, 1)(geom.coords))).to_dict()
        grouped["uuids_geometry"] = grouped["uuids"].map(lambda uuids: itemgetter(*uuids)(roadseg_geometry))
        grouped["uuids_geometry"] = grouped["uuids_geometry"].map(lambda g: g if isinstance(g, tuple) else (g,))

        # Filter associated uuids by validating coordinate subset.
        # Process: for each coordinate set for each uuid in a group, test if the set is a subset of the
        # complete group coordinate set.
        grouped_query = pd.Series(np.vectorize(
            lambda pts_group, pts_uuids: list(map(lambda pts_uuid: pts_uuid.issubset(pts_group), pts_uuids)),
            otypes=[np.object])(
            grouped["geometry"], grouped["uuids_geometry"]))

        # Handle exceptions 1.
        # Identify results without uuid matches. These represents lines which backtrack onto themselves.
        # These records can be removed from the groupings as their junction-based split was in error.
        grouped_no_matches = grouped_query.loc[grouped_query.map(lambda matches: not any(matches))]
        grouped.drop(grouped_no_matches.index, axis=0, inplace=True)
        grouped_query.drop(grouped_no_matches.index, axis=0, inplace=True)
        grouped.reset_index(drop=True, inplace=True)
        grouped_query.reset_index(drop=True, inplace=True)

        # Update grouped uuids to now-reduced list.
        grouped_query_d = grouped_query.to_dict()
        grouped = pd.Series([list(compress(uuids, grouped_query_d[index]))
                             for index, uuids in grouped["uuids"].iteritems()])

        # Assign nid to groups and explode grouped uuids.
        nid_groups = pd.DataFrame({"uuid": grouped, "nid": [uuid.uuid4().hex for _ in range(len(grouped))]})
        nid_groups = nid_groups.explode("uuid")

        # Handle exceptions 2.
        # Identify duplicated uuids. These represent dissolved groupings of two segments forming a loop, where one
        # segment is composed of only 2 points. Therefore, all coordinates in the 2 point segment will be found in the
        # other segment in the dissolved group, creating a duplicate match when filtering associated uuids.
        # Remove duplicate uuids which have also been assigned a non-unique nid.
        duplicated_uuids = nid_groups["uuid"].duplicated(keep=False)
        duplicated_nids = nid_groups["nid"].duplicated(keep=False)
        nid_groups = nid_groups.loc[~(duplicated_uuids & duplicated_nids)]

        # Assign nids to roadseg.
        # Store results.
        nid_groups.index = nid_groups["uuid"]
        self.roadseg.loc[nid_groups.index, "nid"] = nid_groups["nid"].copy(deep=True)
        self.dframes["roadseg"].loc[self.roadseg.index, "nid"] = self.roadseg["nid"].copy(deep=True)

    def roadseg_recover_and_classify_nids(self) -> None:
        """
        1) Recovers NRN roadseg nids from the previous NRN vintage.
        2) Generates 4 nid classification log files: added, retired, modified, confirmed.
        """

        logger.info("Recovering old nids and classifying all nids for table: roadseg.")

        # Copy and filter dataframes.
        roadseg = self.roadseg[[*self.match_fields, "nid", "uuid", "geometry"]].copy(deep=True)
        roadseg_old = self.roadseg_old[[*self.match_fields, "nid", "geometry"]].copy(deep=True)

        # Group by nid.
        roadseg_grouped = helpers.groupby_to_list(roadseg, "nid", "geometry")
        roadseg_old_grouped = helpers.groupby_to_list(roadseg_old, "nid", "geometry")

        # Dissolve grouped geometries.
        roadseg_grouped = roadseg_grouped.map(lambda geoms: geoms[0] if len(geoms) == 1 else linemerge(geoms))
        roadseg_old_grouped = roadseg_old_grouped.map(lambda geoms: geoms[0] if len(geoms) == 1 else linemerge(geoms))

        # Convert series to geodataframes.
        # Restore nid index as column.
        roadseg_grouped = gpd.GeoDataFrame({"nid": roadseg_grouped.index}, geometry=roadseg_grouped.values)
        roadseg_old_grouped = gpd.GeoDataFrame({"nid": roadseg_old_grouped.index}, geometry=roadseg_old_grouped.values)

        # Merge current and old dataframes on geometry.
        merge = pd.merge(roadseg_old_grouped, roadseg_grouped, how="outer", on="geometry", suffixes=("_old", ""),
                         indicator=True)

        # Classify nid groups as: added, retired, modified, confirmed.
        classified_nids = {
            "added": merge.loc[merge["_merge"] == "right_only", "nid"].to_list(),
            "retired": merge.loc[merge["_merge"] == "left_only", "nid_old"].to_list(),
            "modified": list(),
            "confirmed": merge.loc[merge["_merge"] == "both"]
        }

        # Recover old nids for confirmed and modified nid groups.
        # Process: Filter merged dataframes to only those with matches on both, create a lookup dict between the new and
        # old nids.
        recovery = merge.loc[merge["_merge"] == "both"].drop_duplicates(subset="nid", keep="first")
        recovery.index = recovery["nid"]

        # Filter invalid nids from old data.
        recovery = recovery.loc[self.get_valid_ids(recovery["nid_old"])]

        # Recover old nids.
        recovery_lookup = recovery["nid_old"].to_dict()

        if len(recovery_lookup):
            flag = self.roadseg["nid"].isin(recovery_lookup)
            self.roadseg.loc[flag, "nid"] = self.roadseg.loc[flag, "nid"].map(recovery_lookup)

        # Store results.
        self.dframes["roadseg"].loc[self.roadseg.index, "nid"] = self.roadseg["nid"].copy(deep=True)

        # Separate modified from confirmed nid groups.
        # Process: for each of the current and old dataframes, compile the first instance of the NID, then compare the
        # equality of the match fields between the current and old dataframes to determine if a record was modified.
        confirmed_new = classified_nids["confirmed"]\
            .merge(roadseg[["nid", *self.match_fields]], how="left", on="nid")\
            .drop_duplicates(subset="nid", keep="first")
        confirmed_old = classified_nids["confirmed"]\
            .merge(roadseg_old[["nid", *self.match_fields]], how="left", left_on="nid_old", right_on="nid")\
            .drop_duplicates(subset="nid_x", keep="first")

        # Compare match fields to separate modified nid groups.
        # Update modified and confirmed nid classifications.
        flags = (confirmed_new[self.match_fields].values == confirmed_old[self.match_fields].values).all(axis=1)
        classified_nids["modified"] = confirmed_new.loc[~flags, "nid"].to_list()
        classified_nids["confirmed"] = confirmed_new.loc[flags, "nid"].to_list()

        # Store nid classifications as change logs.
        self.change_logs["roadseg"] = {
            change: "\n".join(map(str, ["Records listed by nid:", *nids])) if len(nids) else "No records." for
            change, nids in classified_nids.items()}

    def roadseg_update_linkages(self) -> None:
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
            default = self.defaults["nid"]
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

    def execute(self) -> None:
        """Executes an NRN stage."""

        self.roadseg_gen_full()
        self.roadseg_gen_nids()
        self.roadseg_recover_and_classify_nids()
        self.roadseg_update_linkages()
        self.recover_and_classify_nids()
        self.gen_and_recover_structids()
        self.export_change_logs()
        helpers.export(self.dframes, self.data_path)


@click.command()
@click.argument("source", type=click.Choice("ab bc mb nb nl ns nt nu on pe qc sk yt".split(), False))
@click.option("--remove / --no-remove", "-r", default=False, show_default=True,
              help="Remove pre-existing change logs within the data/processed directory for the specified source.")
def main(source: str, remove: bool = False) -> None:
    """
    Executes an NRN stage.

    :param str source: abbreviation for the source province / territory.
    :param bool remove: removes pre-existing change logs within the data/processed directory for the specified source,
        default False.
    """

    try:

        with helpers.Timer():
            stage = Stage(source, remove)
            stage.execute()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
