import click
import geopandas as gpd
import fiona # DLL error (related to fiona/gdal/geopandas compatibility) requires either gdal or geopandas import first.
import logging
import pandas as pd
import sys
from collections import Counter
from itertools import accumulate, chain
from operator import attrgetter, itemgetter
from pathlib import Path
from shapely import LineString, MultiLineString, Point
from shapely.ops import linemerge
from typing import List, Union

filepath = Path(__file__).resolve()
sys.path.insert(1, str(filepath.parents[3]))
import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class LRS:
    """Class to convert Yukon data from Linear Reference System (LRS) to GeoPackage."""

    def __init__(self, src: Union[Path, str], dst: Union[Path, str]) -> None:
        """
        Initializes the LRS conversion class.

        :param Union[Path, str] src: source path.
        :param Union[Path, str] dst: destination path.
        """

        self.nrn_datasets = dict()
        self.src_datasets = dict()
        self.base_dataset = "tdylrs_centerline_sequence"
        self.geometry_dataset = "tdylrs_centerline"
        self.event_measurement_fields = {"from": "fromkm", "to": "tokm"}

        # Note: listed ids are only for those routes which begin outside of Yukon.
        self.calibrations = {
            "dataset": "tdylrs_calibration_point",
            "id_field": "routeid",
            "measurement_field": "measure",
            "ids": ["004097", "004307", "004349"]
        }

        self.point_datasets = {}
        self.point_event_measurement_field = None

        # Dataset import specifications.
        self.schema = {
            "br_bridge_ln": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "bridge_name"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "bridge_name"]
            },
            "sm_structure": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "surface_code"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "surface_code"]
            },
            "tdylrs_calibration_point": {
                "fields": ["routeid", "fromdate", "todate", "networkid", "measure", "geometry"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999') & networkid==1",
                "output_fields": None
            },
            "tdylrs_centerline": {
                "fields": ["centerlineid", "geometry"],
                "query": None,
                "output_fields": None
            },
            "tdylrs_centerline_sequence": {
                "fields": ["routeid", "fromdate", "todate", "networkid", "centerlineid"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999') & networkid==1",
                "output_fields": ["fromdate"]
            },
            "tdylrs_primary_rte": {
                "fields": ["fromdate", "todate", "routeid", "planimetric_accuracy", "acquisition_technique_dv",
                           "acquired_by_dv", "acquisition_date"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "planimetric_accuracy", "acquisition_technique_dv", "acquired_by_dv",
                                  "acquisition_date"]
            },
            "td_lane_configuration": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "lane_configuration"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "lane_configuration"]
            },
            "td_number_of_lanes": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "number_of_lanes"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "number_of_lanes"]
            },
            "td_road_administration": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "administration"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "administration"]
            },
            "td_road_type": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "road_type"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "road_type"]
            },
            "td_street_name": {
                "fields": ["routeid", "fromdate", "todate", "fromkm", "tokm", "street_direction_prefix",
                           "street_type_prefix", "street_name", "street_type_suffix", "street_direction_suffix"],
                "query": "todate.isna() & ~fromdate.astype('str').str.startswith('9999')",
                "output_fields": ["fromdate", "street_direction_prefix", "street_type_prefix", "street_name",
                                  "street_type_suffix", "street_direction_suffix"]
            }
        }

        # Connections between datasets to the main (base) dataset.
        self.structure = {
            "base": self.base_dataset,
            "connections": {
                "centerlineid": ["tdylrs_centerline"],
                "routeid": ["br_bridge_ln", "sm_structure", "tdylrs_calibration_point", "tdylrs_primary_rte",
                            "td_lane_configuration", "td_number_of_lanes", "td_road_administration", "td_road_type",
                            "td_street_name"]
            }
        }

        # Input dataset columns to be renamed upon import.
        self.rename = {
            "acquired_by_dv": "provider",
            "acquisition_date": "credate",
            "acquisition_technique_dv": "acqtech",
            "administration": "roadjuris",
            "bridge_name": "strunameen",
            "fromdate": "revdate",
            "lane_configuration": "trafficdir",
            "number_of_lanes": "nbrlanes",
            "planimetric_accuracy": "accuracy",
            "road_type": "roadclass",
            "street_direction_prefix": "dirprefix",
            "street_direction_suffix": "dirsuffix",
            "street_name": "namebody",
            "street_type_prefix": "strtypre",
            "street_type_suffix": "strtysuf",
            "surface_code": "pavstatus"
        }

        # Define queries to separate final (NRN) datasets.
        self.final_dataset_separations = {}

        # Validate src.
        self.src = Path(src).resolve()
        if self.src.suffix != ".gdb":
            logger.exception(f"Invalid src input: {src}. Must be a File GeoDatabase.")
            sys.exit(1)

        # Validate dst.
        self.dst = Path(dst).resolve()
        if self.dst.suffix != ".gpkg":
            logger.exception(f"Invalid dst input: {dst}. Must be a GeoPackage.")
            sys.exit(1)
        if self.dst.exists():
            logger.exception(f"Invalid dst input: {dst}. File already exists.")
            sys.exit(1)

    def __call__(self) -> None:
        """Executes class functionality."""

        self.compile_source_datasets()
        self.configure_valid_records()
        self.clean_event_measurements()
        self.assemble_segmented_network()
        self.assemble_network_attribution()
        self.split_at_intersections()
        self.separate_final_datasets()
        self.export_gpkg()

    def assemble_network_attribution(self) -> None:
        """Assembles all required attributes from the source datasets to the segmented road network."""

        def fetch_attr_index(df_sub: pd.DataFrame, con_id: Union[int, str], interval: pd.Interval) -> \
                Union[None, int]:
            """
            Fetches the DataFrame records which matche the connection ID and overlap the breakpoint interval.

            :param pd.DataFrame df_sub: DataFrame.
            :param Union[int, str] con_id: connection ID between df_sub and the base dataset.
            :param pd.Interval interval: Interval representing the breakpoints of an attribute.
            :return Union[None, int]: None or the index of the first DataFrame record which matches the connection ID
                and overlaps the breakpoint interval.
            """

            df_filter = df_sub.loc[df_sub[con_id_field] == con_id]
            indexes = df_filter.loc[df_filter["interval"].map(lambda intv: intv.overlaps(interval))].index
            return indexes[0] if len(indexes) else None

        # Assemble attributes from source datasets.
        logger.info(f"Assembling attributes from source datasets.")

        base = self.nrn_datasets["roadseg"].copy(deep=True)

        # Convert breakpoints to pandas intervals.
        base["interval"] = base["breakpts"].map(lambda vals: pd.Interval(*vals))

        # Iterate source datasets that are connected to the base dataset and have columns to be keep on output.
        for con_id_field, names in self.structure["connections"].items():
            for name in [n for n in names if self.schema[n]["output_fields"]]:

                logger.info(f"Assembling attributes from dataset: {name}.")

                df = self.src_datasets[name].copy(deep=True)

                # Compile required attributes with updated names. Add a suffix to columns already in base dataset.
                # Note: Underscore suffixes are applied to conflicting field names. For certain fields, such as dates,
                # it may be useful to keep multiple instances.
                cols_keep = list()
                for col in self.schema[name]["output_fields"]:
                    col = self.rename[col]
                    while col in base.columns:
                        col += "_"
                        df.rename(columns={col[:-1]: col}, inplace=True)
                    cols_keep.append(col)

                    # Add new column to base dataset.
                    base[col] = None

                # Handle singular (non-segmented) matches.
                # Flag base records and filter attributes dataframe to relevant records.
                # Note: duplicated(keep='first') ensures that one-to-many matches between the base and attribute dataset
                # will still have an attribute record to link to.
                flag_base_a = base[con_id_field].isin(set(df[con_id_field])) & \
                              ~base[con_id_field].duplicated(keep=False)
                df_sub = df.loc[(df[con_id_field].isin(set(base.loc[flag_base_a, con_id_field]))) &
                                (~df[con_id_field].duplicated(keep="first")), [con_id_field, *cols_keep]]

                # Update base dataset with attributes.
                base.loc[flag_base_a, cols_keep] = base.loc[flag_base_a, [con_id_field]].merge(
                    df_sub, how="left", on=con_id_field)[cols_keep].values

                # Handle plural (segmented) matches.
                flag_base_b = False
                if "breakpts" in df.columns:

                    # Flag base records and filter attributes dataframe to relevant records.
                    flag_base_b = base[con_id_field].isin(set(df[con_id_field])) & \
                                  base[con_id_field].duplicated(keep=False)
                    df_sub = df.loc[df[con_id_field].isin(set(base.loc[flag_base_b, con_id_field])),
                                    [con_id_field, "breakpts", *cols_keep]]

                    # Convert breakpoints to pandas intervals.
                    df_sub["interval"] = df_sub["breakpts"].map(lambda vals: pd.Interval(*vals))

                    # Fetch the indexes of the attribute dataset which correspond to the base dataset.
                    args = base.loc[flag_base_b, [con_id_field, "interval"]].apply(list, axis=1)
                    idx = args.map(lambda vals: fetch_attr_index(df_sub, *vals))
                    idx = idx.loc[~idx.isna()]

                    # Update base dataset with attributes by merging the base and attribute datasets.
                    flag_base_b = base.index.isin(set(idx.index))
                    base["idx"] = None
                    base.loc[flag_base_b, "idx"] = idx
                    base.loc[flag_base_b, cols_keep] = base.loc[flag_base_b, ["idx"]].merge(
                        df_sub, how="left", left_on="idx", right_index=True)[cols_keep].values

                # Overwrite non-modified records with Nones to reverse autocasting.
                flag_base = (flag_base_a | flag_base_b)
                base.loc[~flag_base, cols_keep] = None

        # Resolve conflicting attributes.
        # Note: dates are likely the only attributes which require conflict resolution.
        logger.info(f"Resolving conflicting attributes.")

        # Iterate and compile fields with potential conflicts.
        for field, params in {
            "credate": {"func": min, "isdate": True},
            "revdate": {"func": max, "isdate": True}
        }.items():

            cols = [col for col in base.columns if col.find(field) >= 0]

            # Convert date fields to datetime objects.
            if params["isdate"]:
                for col in cols:
                    base[col] = base[col].map(pd.to_datetime).dt.strftime("%Y%m%d")

            # Apply function to conflicting columns, if required.
            if len(cols) > 1:

                logger.info(f"Resolving conflicting attributes for: {field}.")

                # Resolve conflicts into a single attribute.
                base[field] = base[cols].apply(lambda row: params["func"]([v for v in row if not pd.isna(v)]), axis=1)

        # Remove excess fields (keep all defined output fields plus geometry, drop everything else).
        cols_keep = set(map(lambda col: self.rename[col], chain.from_iterable(
            props["output_fields"] for props in self.schema.values() if props["output_fields"]))).union({"geometry"})
        base.drop(columns=set(base.columns)-cols_keep, inplace=True)

        # Store result.
        self.nrn_datasets["roadseg"] = base.copy(deep=True)

    def assemble_segmented_network(self) -> None:
        """Assembles a segmented road network from the breakpoints (event measurements) of the source datasets."""

        calibrations_df = self.src_datasets[self.calibrations["dataset"]]

        def merge_breakpoints_endpoints(breakpts: List[Union[float, int]], geom: Union[LineString, MultiLineString]) \
                -> List[Union[float, int]]:
            """
            Reconfigures breakpts to include the endpoints of all LineStrings.

            :param List[Union[float, int]] breakpts: sequence of breakpts (event measurements).
            :param Union[LineString, MultiLineString] geom: geometry object which represents the breakpts.
            :return List[Union[float, int]]: sequence of breakpts (event measurements), modified to include the
                endpoints of all LineStrings.
            """

            # Compile cumulative geometry lengths as endpoints.
            endpts = [0, geom.length] if isinstance(geom, LineString) else \
                list(accumulate([0, *[g.length for g in geom.geoms]]))

            # Remove breakpoints which are <= 1 unit from an endpoint or outside of the geometry length range (zero to
            # max length). Endpoints include the start and end of every individual LineString in the geometry.
            # Note: some breakpoints could be outside of the geometry length range due to incorrect calibration points.
            breakpts = [breakpt for breakpt in breakpts if any(
                [(endpts[i] + 1) < breakpt < (endpts[i + 1] - 1) for i in range(len(endpts) - 1)])]

            # Return appended and sorted list of breakpoint and endpoints.
            return sorted(chain(breakpts, endpts))

        def segment_geometry(breakpts: List[Union[float, int]], geom: Union[LineString, MultiLineString]) -> \
                Union[LineString, MultiLineString]:
            """
            Segments a (Multi)LineString at a set of breakpoints. To increase splitting accuracy, breakpoints are
            snapped to pre-existing nodes in the geometry, where possible.

            :param List[Union[float, int]] breakpts: sequence of breakpts (event measurements).
            :param Union[LineString, MultiLineString] geom: geometry object which represents the breakpts.
            :return Union[LineString, MultiLineString]: (Multi)LineString, segmented from the original geometry.
            """

            # Return entire geometry if breakpoints cover entire length.
            if breakpts[0] == 0 and round(breakpts[-1]) == round(geom.length):
                return geom

            # Linestring.
            elif isinstance(geom, LineString):

                # Extract coordinates (nodes) from geometry.
                nodes = list(attrgetter("coords")(geom))

                # Configure the index range for all nodes between breakpoints (using bisection search).
                # Note: due to decimal differences, the safe limits are used such that kept nodes will always include
                # one node which exists before and after the first and last breakpoints, respectively.
                low, high = 0, len(nodes)-1
                while abs(high - low) > 1:
                    mid = int(low + ((high - low) / 2))
                    if breakpts[0] > geom.project(Point(nodes[mid])):
                        low = mid
                    else:
                        high = mid
                from_idx = low

                low, high = from_idx, len(nodes)-1
                while abs(high - low) > 1:
                    mid = int(low + ((high - low) / 2))
                    if breakpts[-1] < geom.project(Point(nodes[mid])):
                        high = mid
                    else:
                        low = mid
                to_idx = high + 1

                # Compile nodes from indexes.
                nodes_keep = list(map(Point, nodes[from_idx: to_idx]))

                # Conditionally populate nodes with breakpoints if empty.
                if not len(nodes_keep):
                    nodes_keep = [geom.interpolate(breakpts[0]), geom.interpolate(breakpts[-1])]

                # Conditionally remove nodes more than 1 unit outside the breakpoint range and replace breakpoints with
                # nodes if those nodes are <= 1 unit from the breakpoint.
                else:
                    if abs(breakpts[0] - geom.project(nodes_keep[0])) > 1:
                        nodes_keep = nodes_keep[1:]
                        if abs(breakpts[0] - geom.project(nodes_keep[0])) > 1:
                            nodes_keep = [geom.interpolate(breakpts[0]), *nodes_keep]
                    if abs(breakpts[-1] - geom.project(nodes_keep[-1])) > 1:
                        nodes_keep = nodes_keep[:-1]
                        if abs(breakpts[-1] - geom.project(nodes_keep[-1])) > 1:
                            nodes_keep = [*nodes_keep, geom.interpolate(breakpts[-1])]

                return LineString(nodes_keep)

            # MultiLineString.
            else:

                geoms = list()

                # Compile cumulative LineString lengths as endpoint ranges.
                endpts = list(accumulate([0, *[g.length for g in geom.geoms]]))
                endpts_rng = [pd.Interval(endpts[i], endpts[i+1]) for i in range(len(endpts)-1)]

                # Iterate breakpoint pairs and extract the corresponding LineString from the MultiLineString.
                for index in range(len(breakpts)-1):
                    breakpts_ = breakpts[index: index+2]
                    geom_idx = 0
                    for idx, endpt_rng in enumerate(endpts_rng):
                        if pd.Interval(*breakpts_).overlaps(endpt_rng):
                            geom_idx = idx
                            break
                    geom_ = geom.geoms[geom_idx]

                    # Subtract from the breakpoints the distance of the LineString start relative to the full
                    # MultiLineString.
                    if geom_idx > 0:
                        sub = sum(g.length for g in geom.geoms[:geom_idx].geoms)
                        breakpts_ = [breakpt - sub for breakpt in breakpts]

                    # Call this function with the new parameters, append results to geometry list.
                    geoms.append(segment_geometry(breakpts_, geom_))

                return MultiLineString(geoms)

        def sort_multilinestring(con_id: Union[int, str], geom: MultiLineString) -> MultiLineString:
            """
            Sorts a MultiLineString into the correct LineString ordering based on calibration points.

            :param Union[int, str] con_id: connection ID between the calibrations dataset and the base dataset.
            :param MultiLineString geom: MultiLineString.
            :return MultiLineString: sorted MultiLineString.
            """

            # Compile sorted calibration points for connection ID.
            calibration_pts = calibrations_df.loc[calibrations_df[self.calibrations["id_field"]] == con_id] \
                .sort_values(self.calibrations["measurement_field"])

            # Get LineString index order by intersecting calibration points with LineStrings.
            index_order = list(dict.fromkeys(chain.from_iterable(calibration_pts["geometry"].map(
                lambda pt: [index for index, line in enumerate(geom.geoms) if pt.intersects(line)]).to_list())))

            # Add missing indexes.
            # Note: indexes will not be missing with topologically correct geometries, however, these errors have been
            # identified in the data and it is preferred to accommodate them here and flag them collectively in the
            # actual NRN pipeline.
            missing = set(range(len(geom.geoms))) - set(index_order)
            index_order.extend(missing)

            # Create MultiLineString from LineString index ordering.
            return MultiLineString(itemgetter(*index_order)(geom.geoms))

        logger.info("Assembling segmented network.")

        # Assemble base - geometry connection.
        logger.info(f"Assembling base - geometry connection: {self.base_dataset} - {self.geometry_dataset}.")

        # Assemble datasets if they are not the same.
        base = self.src_datasets[self.base_dataset].copy(deep=True)
        if self.base_dataset != self.geometry_dataset:
            base = gpd.GeoDataFrame(base.merge(self.src_datasets[self.geometry_dataset], how="left",
                                               on=self.get_con_id_field(self.geometry_dataset)))

        # Explode geometries to singlepart.
        base = helpers.explode_geometry(base)

        # Merge geometries for many-to-one links; keep only the first record but keep the entire merged geometry.
        con_id_field = self.calibrations["id_field"]
        flag = base[con_id_field].duplicated(keep=False)
        geom_links = dict(base.loc[flag][[con_id_field, "geometry"]]
                          .groupby(by=con_id_field, axis=0, as_index=True)["geometry"].agg(tuple)
                          .map(linemerge))
        base = base.loc[~base[con_id_field].duplicated(keep="first")]
        base.loc[flag, "geometry"] = base.loc[flag, con_id_field].map(geom_links)

        # Sort MultiLineStrings into proper LineString ordering.
        logger.info(f"Sorting MultiLineStrings into proper LineString ordering.")

        con_id_field = self.calibrations["id_field"]
        flag = base.geom_type == "MultiLineString"
        base.loc[flag, "geometry"] = base.loc[flag, [con_id_field, "geometry"]].apply(
            lambda row: sort_multilinestring(*row), axis=1)

        # Iterate datasets and assemble all event measurements for each base geometry.
        logger.info(f"Compiling all event measurements as breakpoints.")

        for name, df in self.src_datasets.items():
            if name not in {self.base_dataset, self.geometry_dataset} and {"from", "to"}.issubset(set(df.columns)):
                logger.info(f"Compiling breakpoints for dataset: {name}.")

                # Identify connection field.
                con_id_field = self.get_con_id_field(name)

                # Compile breakpoints as flattened list.
                df["breakpts"] = df[["from", "to"]].apply(list, axis=1)
                breakpts = df[[con_id_field, "breakpts"]].groupby(by=con_id_field, axis=0, as_index=True)["breakpts"]\
                    .agg(tuple).map(chain.from_iterable).map(tuple)

                # Merge breakpoints with base dataset.
                breakpts.name = f"{name}_breakpts"
                base = base.merge(breakpts, how="left", left_on=con_id_field, right_index=True)

        # Reduce and sort breakpoints into flattened lists.
        logger.info(f"Reducing and sorting breakpoints.")

        breakpt_cols = [col for col in base.columns if col.endswith("_breakpts")]
        base["breakpts"] = base[breakpt_cols].apply(
            lambda row: chain.from_iterable(r for r in row if isinstance(r, tuple)), axis=1).map(set).map(sorted)

        # Remove extraneous columns.
        base.drop(columns=breakpt_cols, inplace=True)

        # Filter breakpoints which are too close together.
        logger.info(f"Filtering breakpoints which are too close together.")

        # Filter breakpoints by keeping only those which are more than 1 unit distance from the next breakpoint.
        flag = base["breakpts"].map(len) >= 2
        base.loc[flag, "breakpts"] = base.loc[flag, "breakpts"].map(
            lambda pts: [*[pt for index, pt in enumerate(pts[:-1]) if
                           abs(round(pt) - round(pts[index+1])) > 1], pts[-1]])

        # Add geometry start- and endpoints (collectively referred to as endpoints), for all constituent LineStrings.
        # Note: remove breakpoints which are within 1 unit distance from the endpoints.
        logger.info(f"Adding geometry endpoints to breakpoints.")

        args = base[["breakpts", "geometry"]].apply(list, axis=1)
        base["breakpts"] = args.map(lambda vals: merge_breakpoints_endpoints(*vals))

        # Split record geometries on breakpoints.
        logger.info(f"Splitting records on geometry breakpoints.")

        # Nest breakpoints into groups of 2.
        base["breakpts"] = base["breakpts"].map(lambda pts: [[pts[i], pts[i+1]] for i in range(len(pts)-1)])

        # Explode dataframe on breakpoints.
        # Note: must use pandas dataframe since geodataframe.explode is geometry based.
        base = gpd.GeoDataFrame(pd.DataFrame(base).explode("breakpts", ignore_index=True))

        # Extract geometry segment corresponding to breakpoints.
        # Nest geometry and breakpoints to use map.
        # Note: for unique connection IDs, keep the entire geometry.
        args = base[["breakpts", "geometry"]].apply(list, axis=1)
        base["geometry"] = args.map(lambda vals: segment_geometry(*vals))

        # Store result.
        self.nrn_datasets["roadseg"] = base.copy(deep=True)

    def clean_event_measurements(self) -> None:
        """
        Performs several cleanup operations on records based on event measurement:
        1. Simplifies event measurement field names to 'from' and 'to'.
        2. Converts measurements to crs unit (current conversion = km to m).
        3. Drops records with invalid measurements (from >= to).
        4. Matches event measurements to any corresponding calibration point measurements (for improved accuracy).
        5. Removes event measurement offsets for out-of-scope records: some records do not start at zero because they
        begin outside of the territory. The event measurements on these records must be reduced according to the
        starting offset.
        6. Repairs gaps in event measurements along the same connected feature.
        7. Flags overlapping event measurements along the same connected feature.
        """

        calibrations_df = self.src_datasets[self.calibrations["dataset"]]

        def match_calibration_pts(con_id: Union[int, str], event: Union[float, int]) -> Union[float, int]:
            """
            Swaps an event measurement for a corresponding calibration point measurements, if possible.

            :param Union[int, str] con_id: connection ID between the source dataset and the calibrations dataset.
            :param Union[float, int] event: measurement breakpoint.
            :return Union[float, int]: measurement breakpoint, possibly adjusted to the nearest calibration value.
            """

            # Filter calibration point to connection ID.
            measurements = calibrations_df.loc[calibrations_df[self.calibrations["id_field"]] == con_id,
                                               self.calibrations["measurement_field"]]

            # Identify matching calibration points for event (tolerance = 1 unit).
            matching_measurements = measurements.loc[measurements.subtract(event).abs() <= 1]
            if len(matching_measurements):
                return matching_measurements.iloc[0]
            else:
                return event

        logger.info("Cleaning event measurement fields.")

        # Compile offsets for event measurements.
        offsets = dict()
        id_field, offset_field = itemgetter("id_field", "measurement_field")(self.calibrations)

        # Convert calibration point measurement units identically to event measurements.
        self.src_datasets[self.calibrations["dataset"]][offset_field] = self.src_datasets[
            self.calibrations["dataset"]][offset_field].multiply(1000)

        # Compile offsets for out-of-scope events.
        offsets_df = calibrations_df.loc[calibrations_df[id_field].isin(self.calibrations["ids"])]
        for offset_id in set(offsets_df[id_field]):
            offsets[offset_id] = offsets_df.loc[offsets_df[id_field] == offset_id, offset_field].min()

        # Iterate dataframes with event measurement fields.
        fields = self.event_measurement_fields

        for layer, df in self.src_datasets.items():
            if set(fields.values()).issubset(df.columns):

                logger.info(f"Cleaning event measurements for dataset: {layer}.")

                # Identify connection field.
                con_id_field = self.get_con_id_field(layer)

                # Convert measurements.
                logger.info("Converting event measurements.")

                df[list(fields.values())] = df[fields.values()].multiply(1000)
                df.rename(columns={fields["from"]: "from", fields["to"]: "to"}, inplace=True)

                # Remove records with invalid event measurements.
                logger.info("Removing records with invalid event measurements.")

                count = len(df)
                df = df.loc[df["from"] < df["to"]].copy(deep=True)
                logger.info(f"Dropped {count - len(df)} of {count} records.")

                # Match event measurements to calibration points, if possible.
                logger.info(f"Matching event measurements against calibration points.")

                count = 0
                for fld in {"from", "to"}:
                    orig = df[fld].copy(deep=True)

                    flag = df[fld] != 0
                    df.loc[flag, fld] = df.loc[flag, [con_id_field, fld]].apply(
                        lambda row: match_calibration_pts(*row), axis=1)

                    count += sum(orig != df[fld])

                logger.info(f"Matched {count} event measurements to calibration points.")

                # Update out-of-scope offsets.
                logger.info("Updating out-of-scope offsets for events measurements.")

                for offset_id, offset in offsets.items():
                    flag = df[con_id_field] == offset_id
                    df.loc[flag, ["from", "to"]] = df.loc[flag, ["from", "to"]].subtract(offset)

                    logger.info(f"Updated {sum(flag)} offset event measurements for {con_id_field}={offset_id}.")

                # Repair gaps in measurement ranges.
                logger.info("Repairing event measurement gaps.")

                # Iterate records with duplicated connection ids.
                update_count = 0
                dup_con_ids = set(df.loc[df[con_id_field].duplicated(keep=False), con_id_field])
                for con_id in dup_con_ids:
                    records = df.loc[df[con_id_field] == con_id]
                    from_min = records["from"].min()

                    # For any gaps (tolerance = 1 unit), reduce the 'from' measurement to the appropriate neighbouring
                    # 'to' measurement.
                    for index, from_value in records.loc[records["from"] != from_min, "from"].iteritems():
                        neighbour = records.loc[(records.index != index) & ((from_value - records["to"]).between(0, 1))]
                        if len(neighbour):

                            # Update record.
                            df.loc[index, "from"] = neighbour["to"].iloc[0]
                            update_count += 1

                logger.info(f"Repaired {update_count} event measurement gaps.")

                # Flag overlapping measurement ranges.
                logger.info("Identifying overlapping event measurement ranges.")

                # Iterate records with duplicated connection ids.
                for con_id in dup_con_ids:
                    overlap_flag = False

                    # Create intervals from event measurements.
                    intervals = df.loc[df[con_id_field] == con_id, ["from", "to"]].apply(
                        lambda row: pd.Interval(*row), axis=1).to_list()

                    # Flag connection id if overlapping intervals are detected.
                    for idx, i1 in enumerate(intervals):
                        for i2 in intervals[idx + 1:]:
                            if i1.overlaps(i2):
                                overlap_flag = True
                                break
                        if overlap_flag:
                            break

                    if overlap_flag:
                        logger.warning(f"Overlap detected: {con_id_field}={con_id}.")

                # Store results.
                self.src_datasets[layer] = df.copy(deep=True)

    def compile_source_datasets(self) -> None:
        """Loads raw source layers into (Geo)DataFrames."""

        logger.info(f"Compiling source datasets from: {self.src}.")

        # Compile layer names for lowercase lookup.
        layers_lower = {name.lower(): name for name in fiona.listlayers(self.src)}

        # Iterate LRS schema.
        for index, items in enumerate(self.schema.items()):

            layer, attr = itemgetter(0, 1)(items)

            logger.info(f"Compiling source dataset {index + 1} of {len(self.schema)}: {layer}.")

            # Load layer into dataframe, force lowercase column names.
            df = gpd.read_file(self.src, driver="OpenFileGDB", layer=layers_lower[layer]).rename(columns=str.lower)

            # Filter columns.
            df.drop(columns=df.columns.difference(attr["fields"]), inplace=True)

            # Filter records with query.
            if attr["query"]:
                count = len(df)
                df.query(attr["query"], inplace=True)
                logger.info(f"Dropped {count - len(df)} of {count} records for dataset: {layer}, based on query.")

            # Update column names to match NRN.
            df.rename(columns=self.rename, inplace=True)

            # Convert tabular dataframes.
            if ("geometry" not in df.columns) or (not df["geometry"].iloc[0]):
                df = pd.DataFrame(df[df.columns.difference(["geometry"])])

            # Store results.
            self.src_datasets[layer] = df.copy(deep=True)

    def configure_valid_records(self) -> None:
        """
        Filters records to only those which link to the base dataset, non-matching datasets are removed.
        Flags many-to-one linkages between the base and geometry datasets.
        """

        logger.info(f"Configuring valid records.")

        # Iterate dataframes and remove records which do not link to the base dataset.
        for name, df in {k: v for k, v in self.src_datasets.items() if k != self.base_dataset}.items():

            logger.info(f"Configuring valid records for source dataset: {name}.")

            # Identify connection field.
            con_id_field = self.get_con_id_field(name)

            # Compile valid IDs from base dataset for the identified connection field.
            valid_ids = set(self.src_datasets[self.base_dataset][con_id_field])

            # Remove records with invalid connection IDs.
            df_valid = df.loc[df[con_id_field].isin(valid_ids)]
            logger.info(f"Dropped {len(df) - len(df_valid)} of {len(df)} records for dataset: {name}, based on ID "
                        f"field: {con_id_field}.")

            # Flag many-to-one linkages between base and geometry datasets, if they are not the same.
            if (name == self.geometry_dataset) and (self.base_dataset != self.geometry_dataset):

                # Compile and flag many-to-one linkages.
                base = self.src_datasets[self.base_dataset]
                for con_id, count in Counter(base.loc[base[con_id_field].duplicated(keep=False), con_id_field]).items():
                    logger.warning(f"Many-to-one linkage identified between base ({self.base_dataset}) and geometry "
                                   f"({self.geometry_dataset}) datasets: {con_id_field}={con_id}, count={count}.")

            # Store or remove dataset.
            if len(df_valid):
                self.src_datasets[name] = df_valid.copy(deep=True)
            else:
                del self.src_datasets[name]

    def export_gpkg(self) -> None:
        """Exports the NRN datasets to a GeoPackage."""

        logger.info("Exporting datasets to GeoPackage.")

        # Iterate datasets.
        for table, df in self.nrn_datasets.items():

            # Conditionally explode geometries.
            geom_types = set(df.geom_type)
            if any(geom_type in geom_types for geom_type in {"MultiPoint", "MultiLineString"}):
                self.nrn_datasets[table] = helpers.explode_geometry(df).copy(deep=True)

        # Export to GeoPackage.
        helpers.export(self.nrn_datasets, self.dst, merge_schemas=True)

    def get_con_id_field(self, name: str) -> str:
        """
        Fetches the connection ID field, relative to the base dataset, for the given dataset name.

        :param str name: dataset name.
        :return str: connection ID field, relative to the base dataset.
        """

        for con_field, df_names in self.structure["connections"].items():
            if name in df_names:
                return con_field

    def separate_final_datasets(self):
        """Separates the final NRN datasets into multiple NRN datasets based on queries."""

        logger.info(f"Separating final NRN datasets.")

        # Iterate NRN datasets to be separated.
        for nrn_dataset, new_datasets in self.final_dataset_separations.items():
            logger.info(f"Separating NRN dataset: \"{nrn_dataset}\".")
            nrn_df = self.nrn_datasets[nrn_dataset]

            # Iterate new dataset parameters and store resulting dataframe.
            for new_dataset in new_datasets:
                name, query = itemgetter("dataset_name", "query")(new_dataset)
                self.nrn_datasets[name] = nrn_df.query(query).copy(deep=True)

                logger.info(f"Separated {len(self.nrn_datasets[name])} records from \"{nrn_dataset}\" to create NRN "
                            f"dataset \"{name}\".")

    def split_at_intersections(self) -> None:
        """
        Splits geometries at nodes, excluding start and endpoints, which are shared by one or more other geometries.
        Intersections without a common node will not be split since it is impossible to determine whether the geometries
        actually intersect or just cross at different elevations.
        """

        def split_geometry_indexes(geom: LineString, indexes: List[int]) -> List[LineString]:
            """
            Splits a LineString at the given node indexes.

            :param LineString geom: LineString.
            :param List[int] indexes: list of node indexes at which the LineString will be split.
            :return List[LineString]: list of LineStrings, segemented from the original geometry.
            """

            # Compile LineString coordinates as splitting Points.
            nodes = list(map(Point, attrgetter("coords")(geom)))

            # Add start and end to indexes and create ordered pairs.
            indexes = [0, *indexes, len(nodes)-1]
            indexes = [[indexes[idx], indexes[idx+1]] for idx in range(len(indexes)-1)]

            # Generate LineStrings from node index ranges.
            return [LineString(nodes[idx_rng[0]: idx_rng[-1]+1]) for idx_rng in indexes]

        logger.info(f"Splitting geometries at intersections.")

        roads = self.nrn_datasets["roadseg"].copy(deep=True)

        # Explode MultiLineStrings.
        roads = helpers.explode_geometry(roads).copy(deep=True)

        # Extract and explode LineStrings to points, filter to only duplicates.
        pts = roads["geometry"].map(attrgetter("coords")).map(tuple).explode()
        pts_dups = set(pts.loc[pts.duplicated(keep=False)])

        # For each LineString, excluding endpoints, compile the point indexes which are duplicated.
        # Note: it does not matter whether the point is duplicated by another LineString or by the same LineString, the
        # geometry should be split regardless.
        roads["node_idxs"] = roads["geometry"].map(
            lambda g: [index + 1 for index, pt in enumerate(tuple(attrgetter("coords")(g))[1:-1]) if pt in pts_dups])

        # Split segments at node indexes.
        split_flag = roads["node_idxs"].map(len) > 0
        args = roads.loc[split_flag, ["geometry", "node_idxs"]].apply(lambda row: [*row], axis=1)

        roads_crs = roads.crs
        roads = pd.DataFrame(roads)
        roads["geometry"] = roads["geometry"].map(lambda g: [g])

        roads.loc[split_flag, "geometry"] = args.map(lambda vals: split_geometry_indexes(*vals))
        logger.info(f"Split {len(args)} records into {sum(roads.loc[split_flag, 'node_idxs'].map(len)+1)} records.")

        # Explode segmented records.
        roads = gpd.GeoDataFrame(roads.explode("geometry", ignore_index=True), crs=roads_crs)

        # Drop excess fields.
        roads.drop(columns=["node_idxs"], inplace=True)

        # Store result.
        self.nrn_datasets["roadseg"] = roads.copy(deep=True)


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.option("--dst", type=click.Path(exists=False), default=filepath.parents[4] / "data/raw/yt/yt.gpkg",
              show_default=True)
def main(src: Union[Path, str], dst: Union[Path, str] = filepath.parents[4] / "data/raw/yt/yt.gpkg") -> None:
    """
    Executes the LRS class.

    \b
    :param Union[Path, str] src: source path.
    :param Union[Path, str] dst: destination path,
        default = Path(__file__).resolve().parents[4] / 'data/raw/yt/yt.gpkg'.
    """

    try:

        with helpers.Timer():
            lrs = LRS(src, dst)
            lrs()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
