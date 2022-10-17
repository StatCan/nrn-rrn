import click
import fiona
import geopandas as gpd
import logging
import math
import numpy as np
import pandas as pd
import re
import shutil
import sys
import uuid
import zipfile
from copy import deepcopy
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from tabulate import tabulate
from tqdm import tqdm
from tqdm.auto import trange
from typing import List, Tuple, Union

filepath = Path(__file__).resolve()
sys.path.insert(1, str(filepath.parents[1]))
import field_map_functions
import helpers
from gen_junctions import Junction
from segment_addresses import Segmentor


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class Conform:
    """Defines an NRN process."""

    def __init__(self, source: str, remove: bool = False, exclude_old: bool = False) -> None:
        """
        Initializes an NRN process.

        :param str source: abbreviation for the source province / territory.
        :param bool remove: removes pre-existing files within the data/interim directory for the specified source,
            default False.
        :param bool exclude_old: sets parameter remove=True, excluding the previous NRN vintage
            (data/interim/source_old.gpkg) for the specified source.
        """

        self.source = source.lower()
        self.remove = remove
        self.exclude_old = exclude_old
        if self.exclude_old:
            self.remove = exclude_old

        # Configure data paths.
        self.src = filepath.parents[2] / f"data/raw/{self.source}"
        self.dst = filepath.parents[2] / f"data/interim/{self.source}.gpkg"
        self.src_old = {ext: filepath.parents[2] / f"data/interim/{self.source}_old.{ext}" for ext in ("gpkg", "zip")}

        # Configure attribute paths.
        self.source_attribute_path = filepath.parent / f"sources/{self.source}"
        self.source_attributes = dict()
        self.target_attributes = dict()

        # Configure DataFrame collections.
        self.source_gdframes = dict()
        self.target_gdframes = dict()

        # Validate and conditionally clear output namespace.
        namespace = list(filter(Path.is_file, self.dst.parent.glob(f"{self.source}[_.]*")))

        if len(namespace):
            logger.warning("Output namespace already occupied.")

            if self.remove:
                logger.warning("Parameter remove=True: Removing conflicting files.")

                for f in namespace:

                    # Conditionally exclude previous NRN vintage.
                    if self.exclude_old and f.name == self.src_old["gpkg"].name:
                        logger.info(f"Parameter exclude-old=True: Excluding conflicting file from removal: \"{f}\".")
                        continue

                    # Remove files.
                    logger.info(f"Removing conflicting file: \"{f}\".")
                    f.unlink()

            else:
                logger.exception("Parameter remove=False: Unable to proceed while output namespace is occupied. Set "
                                 "remove=True (-r) or manually clear the output namespace.")
                sys.exit(1)

        # Configure field defaults, dtypes, and domains.
        self.defaults = helpers.compile_default_values()
        self.dtypes = helpers.compile_dtypes()
        self.domains = helpers.compile_domains()

    def __call__(self) -> None:
        """Executes an NRN process."""

        self.download_previous_vintage()
        self.compile_source_attributes()
        self.compile_target_attributes()
        self.gen_source_dataframes()
        self.segment_addresses()
        self.gen_target_dataframes()
        self.apply_field_mapping()
        self.split_strplaname()
        self.recover_missing_datasets()
        self.apply_domains()
        self.clean_datasets()
        self.filter_and_relink_strplaname()
        self.gen_junctions()
        helpers.export(self.target_gdframes, self.dst)

    def apply_domains(self) -> None:
        """Applies domain restrictions to each column in the target (Geo)DataFrames."""

        logger.info("Applying field domains.")

        table = None
        field = None

        # Instantiate progress bar.
        domains_pbar = trange(sum([len(self.domains[table]) for table in self.target_gdframes]),
                              desc="Applying field domains.", bar_format="{desc}|{bar}| {percentage:3.0f}% {r_bar}")

        try:

            for table in self.target_gdframes:
                for field, domain in self.domains[table].items():

                    domains_pbar.set_description(f"Applying field domains. Current table: {table}. Current field: "
                                                 f"{field}")

                    # Copy series as object dtype.
                    series_orig = self.target_gdframes[table][field].copy(deep=True).astype(object)

                    # Apply domain to series.
                    series_new = helpers.apply_domain(series_orig, domain=domain["lookup"],
                                                      default=self.defaults[table][field])

                    # Force adjust data type.
                    series_new = series_new.map(lambda val: helpers.cast_dtype(val, dtype=self.dtypes[table][field],
                                                                               default=self.defaults[table][field]))

                    # Store results to target dataframe.
                    self.target_gdframes[table][field] = series_new.copy(deep=True)

                    # Compile and log modifications.
                    flag_mods = series_orig.astype(str) != series_new.astype(str)
                    if flag_mods.any():

                        # Compile and quantify modifications.
                        mods = pd.DataFrame({"From": series_orig[flag_mods], "To": series_new[flag_mods]})\
                            .fillna("None").value_counts(sort=True).reset_index(name="Count")
                        mods["Count"] = mods["Count"].map(lambda val: f"{val:,}")

                        # Log modifications.
                        tbl = tabulate(mods.values, headers=mods.columns, tablefmt="rst")
                        domains_pbar.clear()
                        logger.warning(f"Values have been modified for {table}.{field}:\n" + tbl)
                        domains_pbar.refresh()

                    # Update progress bar.
                    domains_pbar.update(1)

        except (AttributeError, KeyError, ValueError):
            logger.exception(f"Invalid schema definition for {table}.{field}.")
            sys.exit(1)

        # Close progress bar.
        domains_pbar.close()

    def apply_field_mapping(self) -> None:
        """Maps the source (Geo)DataFrames to the target (Geo)DataFrames via user-specific field mapping functions."""

        logger.info("Applying field mapping.")

        # Retrieve source attributes and dataframe.
        for source_name, source_attributes in self.source_attributes.items():
            source_gdf = self.source_gdframes[source_name]

            # Retrieve target attributes.
            for target_name in source_attributes["conform"]:

                # Retrieve table field mapping attributes.
                maps = source_attributes["conform"][target_name]

                # Instantiate progress bar.
                fields_pbar = tqdm(maps.items(), total=len(maps), bar_format="{desc}|{bar}| {percentage:3.0f}% {r_bar}")

                # Field mapping.
                for target_field, source_field in fields_pbar:
                    fields_pbar.set_description(f"Applying field mapping to {target_name}. Current field: "
                                                f"{target_field}")

                    # Retrieve target dataframe.
                    target_gdf = self.target_gdframes[target_name]

                    # No mapping.
                    if source_field is None:
                        pass

                    # Raw value mapping.
                    elif isinstance(source_field, (str, int, float)) and str(source_field).lower() not in \
                            source_gdf.columns:

                        # Update target dataframe with raw value.
                        target_gdf[target_field] = source_field

                    # Function mapping.
                    else:

                        # Restructure mapping dict for direct field mapping in case of string or list input.
                        if isinstance(source_field, (str, list)):
                            source_field = {
                                "fields": source_field if isinstance(source_field, list) else [source_field],
                                "functions": [{"function": "direct"}]
                            }

                        # Convert fields to lowercase.
                        if isinstance(source_field["fields"], list):
                            source_field["fields"] = list(map(str.lower, source_field["fields"]))
                        else:
                            source_field["fields"] = list(map(str.lower, [source_field["fields"]]))

                        # Create mapped dataframe from source and target dataframes, keeping only the source fields.
                        mapped_df = pd.DataFrame({field: target_gdf["uuid"].map(
                            source_gdf.set_index("uuid", drop=False)[field]) for field in source_field["fields"]})

                        # Determine if source fields must be processed separately or together.
                        try:
                            process_separately = itemgetter("process_separately")(source_field)
                        except KeyError:
                            process_separately = False

                        # Create dataframe to hold results if multiple fields are given and not processed separately.
                        if not process_separately or len(source_field["fields"]) == 1:
                            results = pd.Series(dtype=object)
                        else:
                            results = pd.DataFrame(columns=range(len(source_field["fields"])))

                        # Iterate source fields.
                        for index, field in enumerate(source_field["fields"]):

                            # Retrieve series from mapped dataframe.
                            if process_separately or len(source_field["fields"]) == 1:
                                mapped_series = mapped_df[field]
                            else:
                                mapped_series = mapped_df.apply(lambda row: row.values, axis=1)

                            # Apply field mapping functions to mapped series.
                            field_mapping_results = self.apply_functions(mapped_series, source_field["functions"])

                            # Store results.
                            if isinstance(results, pd.Series):
                                results = field_mapping_results.copy(deep=True)
                                break
                            else:
                                results[index] = field_mapping_results.copy(deep=True)

                        # Convert results dataframe to series, if required.
                        if isinstance(results, pd.Series):
                            field_mapping_results = results.copy(deep=True)
                        else:
                            field_mapping_results = results.apply(lambda row: row.values, axis=1)

                        # Update target dataframe.
                        target_gdf[target_field] = field_mapping_results.copy(deep=True)

                    # Store updated target dataframe.
                    self.target_gdframes[target_name] = target_gdf.copy(deep=True)

    def apply_functions(self, series: pd.Series, func_list: List[dict]) -> pd.Series:
        """
        Iterates and applies field mapping function(s) to a Series.

        :param pd.Series series: Series.
        :param List[dict] func_list: list of yaml-constructed field mapping definitions passed to
            :func:`field_map_functions`.
        :return pd.Series: mapped Series.
        """

        # Iterate functions.
        for func in func_list:
            func_name = func["function"]
            params = {k: v for k, v in func.items() if k not in {"function", "iterate_cols"}}

            # Generate expression.
            expr = f"field_map_functions.{func_name}(series, **params)"

            try:

                # Iterate nested columns.
                if "iterate_cols" in func and isinstance(series.iloc[0], (np.ndarray, list)):

                    # Unpack nested Series as DataFrame and iterate required columns.
                    df = pd.DataFrame(series.tolist(), index=series.index)
                    for col_index in func["iterate_cols"]:

                        # Execute expression against individual Series.
                        series = df[col_index].copy(deep=True)
                        df[col_index] = eval(expr).copy(deep=True)

                    # Reconstruct nested Series.
                    series = df.apply(lambda row: row.values, axis=1)

                else:

                    # Execute expression.
                    series = eval(expr).copy(deep=True)

            except (IndexError, SyntaxError, ValueError):
                logger.exception(f"Invalid expression: {expr}.")
                sys.exit(1)

        return series

    def clean_datasets(self) -> None:
        """Applies a series of data cleanups to certain datasets."""

        def _enforce_min_value(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Enforces minimum value for NRN attributes: 'accuracy', 'nbrlanes', 'speed'.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            # Define minimum values.
            min_values = {
                "accuracy": 1,
                "nbrlanes": 1,
                "speed": 1
            }

            # Iterate columns.
            for col in {"accuracy", "nbrlanes", "speed"}.intersection(df.columns):

                # Enforce minimum value.
                series_orig = df[col].copy(deep=True)
                df.loc[df[col] < min_values[col], col] = self.defaults[table][col]

                # Quantify and log modifications.
                mods = (series_orig != df[col]).sum()
                if mods:
                    log += f"Modified {mods} record(s) in {table}.{col}." \
                           f"\nModification details: Values < minimum set to default value.\n"

            return df.copy(deep=True), log

        def _lower_case_ids(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Sets all ID fields to lower case.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            # Iterate columns which a) end with "id", b) are str type, and c) are not uuid.
            dtypes = self.dtypes[table]
            for col in [fld for fld in df.columns.difference(["uuid"]) if fld.endswith("id") and dtypes[fld] == "str"]:

                # Filter records to non-default values which are not already lower case.
                default = self.defaults[table][col]
                s_filtered = df.loc[df[col].map(lambda val: val != default and not val.islower()), col]

                # Apply modifications, if required.
                if len(s_filtered):
                    df.loc[s_filtered.index, col] = s_filtered.map(str.lower)

                    # Quantify and log modifications.
                    log += f"Modified {len(s_filtered)} record(s) in {table}.{col}." \
                           f"\nModification details: Values set to lower case.\n"

            return df.copy(deep=True), log

        def _overwrite_segment_ids(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Populates the NRN attributes 'ferrysegid' or 'roadsegid', whichever appropriate, with incrementing integer
            values from 1-n.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            if table in {"ferryseg", "roadseg"}:

                # Overwrite column.
                col = {"ferryseg": "ferrysegid", "roadseg": "roadsegid"}[table]
                df[col] = range(1, len(df) + 1)

            return df.copy(deep=True), log

        def _resolve_date_order(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Resolves conflicts between credate and revdate by swapping values where credate > revdate.
            Exception for 'revdate = 0', since this is valid.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""
            df_orig = df.copy(deep=True)

            # Filter to non-default dates and non-zero revdates.
            defaults = {"credate": self.defaults[table]["credate"],
                        "revdate": self.defaults[table]["revdate"]}
            df = df.loc[(df["credate"] != defaults["credate"]) &
                        (~df["revdate"].isin({defaults["revdate"], 0})), ["credate", "revdate"]].copy(deep=True)

            # Temporarily populate incomplete dates with "01" suffix.
            for col in ("credate", "revdate"):
                for length in (4, 6):
                    flag = df[col].map(lambda val: int(math.log10(val)) + 1) == length
                    if length == 4:
                        df.loc[flag, col] = df.loc[flag, col].map(lambda val: (val * 10000) + 101)
                    else:
                        df.loc[flag, col] = df.loc[flag, col].map(lambda val: (val * 100) + 1)

            # Flag records with invalid date order.
            flag = df["credate"] > df["revdate"]
            if sum(flag):

                # Swap dates.
                df_orig.loc[flag.index, ["credate", "revdate"]] = \
                    df_orig.loc[flag.index, ["revdate", "credate"]].copy(deep=True)

                # Log modifications.
                mods = sum(flag)
                log += f"Modified {mods} record(s) in {table}.credate/revdate." \
                       f"\nModification details: Swapped values.\n"

            return df_orig.copy(deep=True), log

        def _resolve_pavsurf(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Resolves conflicts between pavstatus and pavsurf / unpavsurf.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            if table == "roadseg":

                paved_orig = df["pavsurf"].copy(deep=True)
                unpaved_orig = df["unpavsurf"].copy(deep=True)

                # For 'Paved' roads:
                # 1) Ensure 'unpavsurf' = 'None'
                # 2) Ensure 'pavsurf' != 'None'.
                flag_paved = (df["pavstatus"] == "Paved")
                df.loc[flag_paved & (df["unpavsurf"] != "None"), "unpavsurf"] = "None"
                df.loc[flag_paved & (df["pavsurf"] == "None"), "pavsurf"] = self.defaults[table]["pavsurf"]

                # For 'Unpaved' roads:
                # 1) Ensure 'pavsurf' = 'None'
                # 2) Ensure 'unpavsurf' != 'None'.
                flag_unpaved = (df["pavstatus"] == "Unpaved")
                df.loc[flag_unpaved & (df["pavsurf"] != "None"), "pavsurf"] = "None"
                df.loc[flag_unpaved & (df["unpavsurf"] == "None"), "unpavsurf"] = self.defaults[table]["unpavsurf"]

                # Log modifications.
                for col, series_orig in (("pavsurf", paved_orig), ("unpavsurf", unpaved_orig)):
                    mods = sum(series_orig != df[col])
                    if mods:
                        log += f"Modified {mods} record(s) in {table}.{col}." \
                               f"\nModification details: Values set to \"None\" / default value.\n"

            return df.copy(deep=True), log

        def _resolve_zero_credates(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Resolves instances of 'credate = 0' by setting to the default value.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""
            df_orig = df.copy(deep=True)

            # Flag records with credate = 0.
            flag = df["credate"] == 0
            if sum(flag):

                # Set values to default.
                df_orig.loc[flag.index, "credate"] = self.defaults[table]["credate"]

                # Log modifications.
                mods = sum(flag)
                log += f"Modified {mods} record(s) in {table}.credate." \
                       f"\nModification details: Set instances of \"0\" to default value.\n"

            return df_orig.copy(deep=True), log

        def _standardize_nones(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Standardizes string 'None's (distinct from Null).

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            # Compile valid columns.
            cols = df.select_dtypes(include="object", exclude="geometry").columns.values

            # Iterate columns.
            for col in cols:

                # Apply modifications.
                series_orig = df[col].copy(deep=True)
                df.loc[df[col].map(str.lower) == "none", col] = "None"

                # Quantify and log modifications.
                mods = (series_orig != df[col]).sum()
                if mods:
                    log += f"Modified {mods} record(s) in {table}.{col}." \
                           f"\nModification details: Various None-types standardized to \"None\".\n"

            return df.copy(deep=True), log

        def _strip_whitespace(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Strips leading, trailing, and successive internal whitespace for each (Geo)DataFrame column.

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            # Compile valid columns.
            cols = df.select_dtypes(include="object", exclude="geometry").columns.values

            # Iterate columns.
            for col in cols:

                # Apply modifications.
                series_orig = df[col].copy(deep=True)
                df[col] = df[col].map(lambda val: re.sub(r" +", " ", str(val.strip())))

                # Quantify and log modifications.
                mods = (series_orig != df[col]).sum()
                if mods:
                    log += f"Modified {mods} record(s) in {table}.{col}." \
                           f"\nModification details: Values stripped of leading, trailing, and successive internal " \
                           f"whitespace.\n"

            return df.copy(deep=True), log

        def _title_case_names(table: str, df: Union[gpd.GeoDataFrame, pd.DataFrame]) -> \
                Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]:
            """
            Sets to title case all NRN name attributes:
                ferryseg: rtename1en, rtename1fr, rtename2en, rtename2fr, rtename3en, rtename3fr, rtename4en, rtename4fr
                roadseg: l_placenam, l_stname_c, r_placenam, r_stname_c, rtename1en, rtename1fr, rtename2en, rtename2fr,
                         rtename3en, rtename3fr, rtename4en, rtename4fr, strunameen, strunamefr
                strplaname: namebody, placename

            :param str table: name of an NRN dataset.
            :param Union[gpd.GeoDataFrame, pd.DataFrame] df: (Geo)DataFrame containing the target NRN attribute(s).
            :return Tuple[Union[gpd.GeoDataFrame, pd.DataFrame], Union[str, None]]: Modified (Geo)DataFrame and string
                                                                                    log of changes, if any.
            """

            log = ""

            if table in {"ferryseg", "roadseg", "strplaname"}:

                # Define name fields.
                name_fields = {
                    "ferryseg": ["rtename1en", "rtename1fr", "rtename2en", "rtename2fr", "rtename3en", "rtename3fr",
                                 "rtename4en", "rtename4fr"],
                    "roadseg": ["l_placenam", "l_stname_c", "r_placenam", "r_stname_c", "rtename1en", "rtename1fr",
                                "rtename2en", "rtename2fr", "rtename3en", "rtename3fr", "rtename4en", "rtename4fr",
                                "strunameen", "strunamefr"],
                    "strplaname": ["namebody", "placename"]
                }

                # Iterate columns.
                for col in name_fields[table]:

                    # Filter records to non-default values which are not already title case.
                    default = self.defaults[table][col]
                    s_filtered = df.loc[df[col].map(lambda route: route != default and not route.istitle()), col]

                    # Apply modifications, if required.
                    if len(s_filtered):
                        df.loc[s_filtered.index, col] = s_filtered.map(str.title)

                        # Quantify and log modifications.
                        log += f"Modified {len(s_filtered)} record(s) in {table}.{col}." \
                               f"\nModification details: Values set to title case.\n"

            return df.copy(deep=True), log

        logger.info("Applying cleanup functions.")

        # Define functions and execution order.
        funcs = (_enforce_min_value, _lower_case_ids, _overwrite_segment_ids, _resolve_zero_credates,
                 _resolve_date_order, _resolve_pavsurf, _standardize_nones, _strip_whitespace, _title_case_names)

        # Instantiate progress bar.
        cleanup_pbar = trange(len(self.target_gdframes) * len(funcs), desc="Applying cleanup functions.",
                              bar_format="{desc}|{bar}| {percentage:3.0f}% {r_bar}")

        # Iterate and apply cleanup functions to each dataframe.
        for table, df in self.target_gdframes.items():
            for func in funcs:

                cleanup_pbar.set_description(f"Applying cleanup functions. Current table: {table}. Current function: "
                                             f"{func.__name__}")

                # Parse function results.
                df, log = func(table, df)

                # Log modifications.
                if log:
                    cleanup_pbar.clear()
                    logger.warning(log)
                    cleanup_pbar.refresh()

                # Update progress bar.
                cleanup_pbar.update(1)

            # Store updated dataframe.
            self.target_gdframes.update({table: df.copy(deep=True)})
        cleanup_pbar.close()

    def compile_source_attributes(self) -> None:
        """Compiles the yaml files in the sources' directory into a dictionary."""

        logger.info("Compiling source attribute yamls.")
        self.source_attributes = dict()

        # Iterate source yamls.
        for f in filter(Path.is_file, Path(self.source_attribute_path).glob("*.yaml")):

            # Load yaml and store contents.
            self.source_attributes[f.stem] = helpers.load_yaml(f)

    def compile_target_attributes(self) -> None:
        """Compiles the yaml file for the target (Geo)DataFrames (distribution format) into a dictionary."""

        logger.info("Compiling target attribute yaml.")
        table = field = None

        # Load yaml.
        self.target_attributes = helpers.load_yaml(filepath.parents[1] / "distribution_format.yaml")

        # Remove field length from dtype attribute.
        logger.info("Configuring target attributes.")
        try:

            for table in self.target_attributes:
                for field, vals in self.target_attributes[table]["fields"].items():
                    self.target_attributes[table]["fields"][field] = vals[0]

        except (AttributeError, KeyError, ValueError):
            logger.exception(f"Invalid schema definition for {table}.{field}.")
            sys.exit(1)

    def download_previous_vintage(self) -> None:
        """Downloads the previous NRN vintage and extracts the English GeoPackage as <source>_old.gpkg."""

        logger.info("Retrieving previous NRN vintage.")

        # Determine download requirement.
        if self.src_old["gpkg"].exists():
            logger.warning(f"Previous NRN vintage already exists: \"{self.src_old['gpkg']}\". Skipping step.")

        else:

            # Download previous NRN vintage.
            logger.info("Downloading previous NRN vintage.")
            download_url = None

            try:

                # Get download url.
                download_url = helpers.load_yaml(
                    filepath.parents[1] / "downloads.yaml")["previous_nrn_vintage"][self.source]

                # Get raw content stream from download url.
                download = helpers.get_url(download_url, stream=True, timeout=30, verify=True)

                # Copy download content to file.
                with open(self.src_old["zip"], "wb") as f:
                    shutil.copyfileobj(download.raw, f)

            except (shutil.Error) as e:
                logger.exception(f"Unable to download previous NRN vintage: \"{download_url}\".")
                logger.exception(e)
                sys.exit(1)

            # Extract zipped data.
            logger.info("Extracting zipped data for previous NRN vintage.")

            gpkg_download = [f for f in zipfile.ZipFile(self.src_old["zip"], "r").namelist() if
                             f.lower().startswith("nrn") and Path(f).suffix == ".gpkg"][0]

            with zipfile.ZipFile(self.src_old["zip"], "r") as zip_f:
                with zip_f.open(gpkg_download) as zsrc, open(self.src_old["gpkg"], "wb") as zdst:
                    shutil.copyfileobj(zsrc, zdst)

            # Remove temporary files.
            logger.info("Removing temporary files for previous NRN vintage.")

            if self.src_old["zip"].exists():
                self.src_old["zip"].unlink()

    def filter_and_relink_strplaname(self) -> None:
        """Reduces duplicated records, where possible, in NRN strplaname and repairs the remaining NID linkages."""

        df = self.target_gdframes["strplaname"].copy(deep=True)

        # Filter duplicates.
        logger.info("Filtering duplicates from strplaname.")

        # Define match fields and drop duplicates.
        match_fields = list(df.columns.difference(["uuid", "nid"]))
        df_new = df.drop_duplicates(subset=match_fields, keep="first", inplace=False)

        if len(df) != len(df_new):

            # Store results.
            self.target_gdframes["strplaname"] = df_new.copy(deep=True)

            # Quantify removed duplicates.
            logger.info(f"Dropped {len(df) - len(df_new)} duplicated records from strplaname.")

            # Repair nid linkages.
            logger.info("Repairing strplaname.nid linkages.")

            # Define nid linkages.
            linkages = {
                "addrange": ["l_offnanid", "r_offnanid"],
                "altnamlink": ["strnamenid"]
            }

            # Generate nid lookup dict.
            # Process: group nids by match fields, set first value in each group as index, explode groups, create dict
            # from reversed index and values.
            nids_grouped = df[[*match_fields, "nid"]].groupby(by=match_fields, axis=0, as_index=True)["nid"].agg(tuple)
            nids_grouped.index = nids_grouped.map(itemgetter(0))
            nids_exploded = nids_grouped.explode()
            nid_lookup = dict(zip(nids_exploded.values, nids_exploded.index))

            # Iterate nid linkages.
            for table in set(linkages).intersection(set(self.target_gdframes)):
                for field in linkages[table]:

                    # Repair nid linkage.
                    series = self.target_gdframes[table][field].copy(deep=True)
                    self.target_gdframes[table].loc[series.index, field] = series.map(
                        lambda val: itemgetter(val)(nid_lookup))

                    # Quantify and log modifications.
                    mods_count = (series != self.target_gdframes[table][field]).sum()
                    if mods_count:
                        logger.warning(f"Repaired {mods_count} linkage(s) between strplaname.nid - {table}.{field}.")

    def gen_junctions(self) -> None:
        """Generate the dataset: junction."""

        logger.info(f"Generating dataset: junction.")

        # Instantiate Junction class.
        junction = Junction(
            source=self.source,
            target_attributes=self.target_attributes["junction"],
            roadseg=self.target_gdframes["roadseg"],
            ferryseg=self.target_gdframes["ferryseg"] if "ferryseg" in self.target_gdframes else None
        )

        # Execute Junction class and store results.
        self.target_gdframes["junction"] = junction()

    def gen_source_dataframes(self) -> None:
        """
        Loads raw source data into GeoDataFrames and applies a series of standardizations, most notably:
        1) explode multi-type geometries.
        2) reprojection to NRN standard EPSG:4617.
        3) round coordinate precision to NRN standard 7 decimal places.
        """

        logger.info("Loading source data as dataframes.")
        self.source_gdframes = dict()

        for source, source_yaml in self.source_attributes.items():

            logger.info(f"Loading source data for {source}.yaml: file={source_yaml['data']['filename']}, layer="
                        f"{source_yaml['data']['layer']}.")

            # Load source data into a geodataframe.
            try:

                df = gpd.read_file(self.src / source_yaml["data"]["filename"],
                                   driver=source_yaml["data"]["driver"],
                                   layer=source_yaml["data"]["layer"])

            except fiona.errors.FionaValueError as e:
                logger.exception(f"Unable to load data source.")
                logger.exception(e)
                sys.exit(1)

            # Query dataframe.
            if source_yaml["data"]["query"]:
                try:
                    df.query(source_yaml["data"]["query"], inplace=True)
                except ValueError as e:
                    logger.exception(f"Invalid query: \"{source_yaml['data']['query']}\".")
                    logger.exception(e)
                    sys.exit(1)

            # Force lowercase column names.
            df.columns = map(str.lower, df.columns)

            # Apply spatial data modifications.
            if source_yaml["data"]["spatial"]:

                # Filter invalid geometries.
                df = df.loc[df.geom_type.isin({"Point", "MultiPoint", "LineString", "MultiLineString"})]

                # Cast multi-type geometries.
                df = helpers.explode_geometry(df)

                # Explicitly assign CRS and reproject to EPSG:4617.
                df.set_crs(source_yaml["data"]["crs"], allow_override=True, inplace=True)
                df = df.to_crs("EPSG:4617")

                # Round coordinates to decimal precision = 7 and flatten to 2-dimensions.
                df = helpers.round_coordinates(df, 7)

            # Add uuid field.
            df["uuid"] = [uuid.uuid4().hex for _ in range(len(df))]

            # Store result.
            self.source_gdframes[source] = df.copy(deep=True)

            logger.info("Successfully loaded source data.")

    def gen_target_dataframes(self) -> None:
        """Creates empty (Geo)DataFrames for all applicable output tables."""

        logger.info("Creating target dataframes for applicable tables.")
        self.target_gdframes = dict()

        # Retrieve target table names from source attributes.
        for source, source_yaml in self.source_attributes.items():
            for table in source_yaml["conform"]:

                logger.info(f"Creating target dataframe: {table}.")

                # Spatial.
                if self.target_attributes[table]["spatial"]:

                    # Generate target dataframe from source uuid and geometry fields.
                    gdf = gpd.GeoDataFrame(self.source_gdframes[source][["uuid"]],
                                           geometry=self.source_gdframes[source].geometry,
                                           crs="EPSG:4617")

                # Tabular.
                else:

                    # Generate target dataframe from source uuid field.
                    gdf = pd.DataFrame(self.source_gdframes[source][["uuid"]])

                # Add target field schema.
                gdf = gdf.assign(**{field: pd.Series(dtype=dtype) for field, dtype in
                                    self.target_attributes[table]["fields"].items()})

                # Store result.
                self.target_gdframes[table] = gdf
                logger.info(f"Successfully created target dataframe: {table}.")

        # Log unavailable datasets.
        for table in [t for t in self.target_attributes if t not in self.target_gdframes]:

            logger.warning(f"Source data provides no field mappings for table: {table}.")

    def recover_missing_datasets(self) -> None:
        """
        Recovers missing NRN datasets in the current vintage from the previous vintage.
        Exception: altnamlink, junction.
        """

        # Identify datasets to be recovered.
        recovery_tables = set(self.target_attributes) - set(self.target_gdframes) - {"altnamlink", "junction"}
        if recovery_tables:

            logger.info("Recovering missing datasets from the previous NRN vintage.")

            # Iterate datasets from previous NRN vintage.
            for table, df in helpers.load_gpkg(self.src_old["gpkg"], find=True, layers=recovery_tables).items():

                # Recover non-empty datasets.
                if len(df):

                    logger.info(f"Recovering dataset: {table}.")

                    # Add uuid field.
                    df["uuid"] = [uuid.uuid4().hex for _ in range(len(df))]

                    if isinstance(df, gpd.GeoDataFrame):

                        # Filter invalid geometries.
                        df = df.loc[df.geom_type.isin({"Point", "MultiPoint", "LineString", "MultiLineString"})]

                        # Cast multi-type geometries.
                        df = helpers.explode_geometry(df)

                        # Reproject to EPSG:4617.
                        df = df.to_crs("EPSG:4617")

                        # Round coordinates to decimal precision = 7 and flatten to 2-dimensions.
                        df = helpers.round_coordinates(df, precision=7)

                    # Store result.
                    self.target_gdframes[table] = df.copy(deep=True)

    def segment_addresses(self) -> None:
        """
        Converts address points into segmented attribution for NRN addrange and merges the resulting attributes to the
        source dataset representing NRN roadseg.
        """

        logger.info("Determining address segmentation requirement.")

        address_source = None
        roadseg_source = None
        segment_kwargs = None

        # Identify segmentation parameters and source datasets for roadseg and address points.
        for source, source_yaml in deepcopy(self.source_attributes).items():

            if "segment" in source_yaml["data"]:
                address_source = source
                segment_kwargs = source_yaml["data"]["segment"]

            if "conform" in source_yaml:
                if isinstance(source_yaml["conform"], dict):
                    if "roadseg" in source_yaml["conform"]:
                        roadseg_source = source

        # Trigger address segmentor.
        if all(val is not None for val in [address_source, roadseg_source, segment_kwargs]):

            logger.info(f"Address segmentation required. Beginning segmentation process.")

            # Copy data sources.
            addresses = self.source_gdframes[address_source].copy(deep=True)
            roadseg = self.source_gdframes[roadseg_source].copy(deep=True)

            # Execute segmentor.
            segmentor = Segmentor(source=self.source, addresses=addresses, roadseg=roadseg, **segment_kwargs)
            self.source_gdframes[roadseg_source] = segmentor()

            # Remove address source from attributes and dataframes references.
            # Note: segmented addresses will be joined to roadseg, therefore addrange and roadseg field mapping should
            # be defined within the same yaml.
            del self.source_attributes[address_source]
            del self.source_gdframes[address_source]

        else:
            logger.info("Address segmentation not required. Skipping segmentation process.")

    def split_strplaname(self) -> None:
        """
        Splits NRN strplaname records into multiple records if at least one nested column exists. The first and second
        records will contain the first and second nested values, respectively. NID linkages are repaired for the second
        instance of each split record since the linkage will have been broken.

        This process creates the left- and right-side representation which NRN strplaname is supposed to possess.
        """

        logger.info("Splitting strplaname to create left- and right-side representation.")

        # Compile nested column names.
        sample_value = self.target_gdframes["strplaname"].iloc[0]
        nested_flags = list(map(lambda val: isinstance(val, (np.ndarray, list)), sample_value))
        cols = sample_value.index[nested_flags].to_list()

        if len(cols):

            # Duplicate dataframe as left- and right-side representations.
            df_l = self.target_gdframes["strplaname"].copy(deep=True)
            df_r = self.target_gdframes["strplaname"].copy(deep=True)

            # Iterate nested columns and keep the 1st and 2nd values for left and right dataframes, respectively.
            for col in cols:
                df_l.loc[df_l.index, col] = df_l[col].map(itemgetter(0))
                df_r.loc[df_r.index, col] = df_r[col].map(itemgetter(1))

            # Generate new nids, uuids, and indexes for right dataframe, re-assign uuids as index for left dataframe.
            df_r["nid"] = [uuid.uuid4().hex for _ in range(len(df_r))]
            df_r["uuid"] = [uuid.uuid4().hex for _ in range(len(df_r))]
            df_r.index = df_r["uuid"]
            df_l.index = df_l["uuid"]

            # Update target dataframe.
            self.target_gdframes["strplaname"] = pd.concat([df_l, df_r], ignore_index=False).copy(deep=True)

            # Generate lookup dict between old and new nids for right dataframe.
            nid_lookup = dict(zip(df_l["nid"], df_r["nid"]))

            # Repair nid linkages.
            logger.info("Repairing strplaname.nid linkages.")

            # Define nid linkages.
            linkages = {
                "addrange": ["r_offnanid"]
            }

            # Iterate nid linkages.
            for table in set(linkages).intersection(set(self.target_gdframes)):
                for field in linkages[table]:

                    # Repair nid linkage.
                    series = self.target_gdframes[table][field].copy(deep=True)
                    self.target_gdframes[table].loc[series.index, field] = series.map(
                        lambda val: itemgetter(val)(nid_lookup))

                    # Quantify and log modifications.
                    mods_count = (series != self.target_gdframes[table][field]).sum()
                    if mods_count:
                        logger.warning(f"Repaired {mods_count} linkage(s) between strplaname.nid - {table}.{field}.")

            # Update altnamlink.
            if "altnamlink" in self.target_gdframes:

                logger.info("Updating altnamlink.")

                # Duplicate records.
                df_first = self.target_gdframes["altnamlink"].copy(deep=True)
                df_second = self.target_gdframes["altnamlink"].copy(deep=True)

                # Generate new strnamenids, uuids, and indexes for second dataframe.
                df_second["strnamenid"] = [uuid.uuid4().hex for _ in range(len(df_second))]
                df_second["uuid"] = [uuid.uuid4().hex for _ in range(len(df_second))]
                df_second.index = df_second["uuid"]

                # Update columns, if required.
                df_second["credate"] = datetime.today().strftime("%Y%m%d")
                df_second["revdate"] = self.defaults["altnamlink"]["revdate"]
                df_second["strnamenid"] = df_second["strnamenid"].map(lambda val: itemgetter(nid_lookup)(val))

                # Store results.
                self.target_gdframes["altnamlink"] = pd.concat([df_first, df_second],
                                                               ignore_index=False).copy(deep=True)


@click.command()
@click.argument("source", type=click.Choice("ab bc mb nb nl ns nt nu on pe qc sk yt".split(), False))
@click.option("--remove / --no-remove", "-r", default=False, show_default=True,
              help="Remove pre-existing files within the data/interim directory for the specified source.")
@click.option("--exclude-old / --no-exclude-old", "-e", default=False, show_default=True,
              help="Sets parameter remove=True, excluding the previous NRN vintage (data/interim/source_old.gpkg) for "
                   "the specified source.")
def main(source: str, remove: bool = False, exclude_old: bool = False) -> None:
    """
    Executes an NRN process.

    \b
    :param str source: abbreviation for the source province / territory.
    :param bool remove: removes pre-existing files within the data/interim directory for the specified source, default
        False.
    :param bool exclude_old: sets parameter remove=True, excluding the previous NRN vintage
        (data/interim/source_old.gpkg) for the specified source.
    """

    try:

        with helpers.Timer():
            process = Conform(source, remove, exclude_old)
            process()

    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Exiting program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
