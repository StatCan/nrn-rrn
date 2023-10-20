import datetime
import geopandas as gpd
import fiona # DLL error (related to fiona/gdal/geopandas compatibility) requires either gdal or geopandas import first.
import logging
import numpy as np
import pandas as pd
import random
import requests
import sqlite3
import sys
import time
import yaml
from collections import ChainMap, defaultdict
from itertools import groupby
from operator import attrgetter, itemgetter
from osgeo import ogr, osr
from pathlib import Path
from shapely import LineString, Point
from tqdm import tqdm
from tqdm.auto import trange
from typing import Any, Dict, List, Type, Union


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


# Enable ogr exceptions.
ogr.UseExceptions()


# Define globally accessible variables.
filepath = Path(__file__).resolve()
distribution_format_path = filepath.parent / "distribution_format.yaml"
field_domains_path = {lang: filepath.parent / f"field_domains_{lang}.yaml" for lang in ("en", "fr")}


class Timer:
    """Tracks stage runtime."""

    def __init__(self) -> None:
        """Initializes the Timer class."""

        self.start_time = None

    def __enter__(self) -> None:
        """Starts the timer."""

        logger.info("Started.")
        self.start_time = time.time()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Computes and returns the elapsed time.

        :param Any exc_type: required parameter for __exit__.
        :param Any exc_val: required parameter for __exit__.
        :param Any exc_tb: required parameter for __exit__.
        """

        total_seconds = time.time() - self.start_time
        delta = datetime.timedelta(seconds=total_seconds)
        logger.info(f"Finished. Time elapsed: {delta}.")


def apply_domain(series: pd.Series, domain: dict, default: Any) -> pd.Series:
    """
    Applies a domain restriction to the given Series based on a domain dictionary.
    Replaces missing or invalid values with the default value.

    Non-dictionary domains are treated as Null. Values are left as-is excluding Null types and empty strings, which are
    replaced with the default value.

    :param pd.Series series: Series.
    :param dict domain: dictionary of acceptable domain values.
    :param Any default: default value.
    :return pd.Series: Series with enforced domain restriction.
    """

    # Validate against domain dictionary.
    if isinstance(domain, dict):

        # Convert keys to lowercase strings.
        domain = {str(k).lower(): v for k, v in domain.items()}

        # Configure lookup function, convert invalid values to default.
        def get_value(val: Any) -> Any:
            """
            Retrieves a domain dictionary value for a given key, non-matches return the default value.

            :param Any val: lookup key.
            :return Any: corresponding domain value or the default value.
            """

            try:
                return domain[str(val).lower()]
            except KeyError:
                return default

        # Get values.
        return series.map(get_value)

    else:

        # Convert empty strings and null types to default.
        series.loc[(series.map(str).isin(["", "nan", "-2147483648", "-2147483648.0"])) | (series.isna())] = default
        return series


def cast_dtype(val: Any, dtype: Type, default: Any) -> Any:
    """
    Casts the value to the given numpy dtype.
    Returns the default parameter for invalid or Null values.

    :param Any val: value.
    :param Type dtype: numpy type object to be casted to.
    :param Any default: value to be returned in case of error.
    :return Any: casted or default value.
    """

    try:

        if pd.isna(val) or val == "":
            return default
        else:
            return itemgetter(0)(np.array([val]).astype(dtype))

    except (TypeError, ValueError):
        return default


def compile_default_values(lang: str = "en") -> dict:
    """
    Compiles the default value for each field in each NRN dataset.

    :param str lang: output language: 'en', 'fr'.
    :return dict: dictionary of default values for each attribute of each NRN dataset.
    """

    dft_vals = load_yaml(field_domains_path[lang])["default"]
    dist_format = load_yaml(distribution_format_path)
    defaults = dict()

    try:

        # Iterate tables.
        for name in dist_format:
            defaults[name] = dict()

            # Iterate fields.
            for field, dtype in dist_format[name]["fields"].items():

                # Configure default value.
                key = "label" if dtype[0] == "str" else "code"
                defaults[name][field] = dft_vals[key]

    except (AttributeError, KeyError, ValueError):
        logger.exception(f"Invalid schema definition for one or more yamls:"
                         f"\nDefault values: {dft_vals}"
                         f"\nDistribution format: {dist_format}")
        sys.exit(1)

    return defaults


def compile_domains(mapped_lang: str = "en") -> dict:
    """
    Compiles the acceptable domain values for each field in each NRN dataset. Each domain will consist of the following
    keys:
    1) 'values': all English and French values and keys flattened into a single list.
    2) 'lookup': a lookup dictionary mapping each English and French value and key to the value of the given map
    language. Integer keys and their float-equivalents are both added to accommodate incorrectly casted data.

    :param str mapped_lang: output language: 'en', 'fr'.
    :return dict: dictionary of domain values and lookup dictionary for each attribute of each NRN dataset.
    """

    # Compile field domains.
    domains = defaultdict(dict)

    # Load domain yamls.
    domain_yamls = {lang: load_yaml(field_domains_path[lang]) for lang in ("en", "fr")}

    # Iterate tables and fields with domains.
    for table in domain_yamls["en"]["tables"]:
        for field in domain_yamls["en"]["tables"][table]:

            try:

                # Compile domains.
                domain_en = domain_yamls["en"]["tables"][table][field]
                domain_fr = domain_yamls["fr"]["tables"][table][field]

                # Configure mapped and non-mapped output domain.
                domain_mapped = domain_en if mapped_lang == "en" else domain_fr
                domain_non_mapped = domain_en if mapped_lang != "en" else domain_fr

                # Compile all domain values and domain lookup table, separately.
                if domain_en is None:
                    domains[table][field] = {"values": None, "lookup": None}

                elif isinstance(domain_en, list):
                    domains[table][field] = {
                        "values": sorted(list({*domain_en, *domain_fr}), reverse=True),
                        "lookup": dict([*zip(domain_en, domain_mapped), *zip(domain_fr, domain_mapped)])
                    }

                elif isinstance(domain_en, dict):
                    domains[table][field] = {
                        "values": sorted(list({*domain_en.values(), *domain_fr.values()}), reverse=True),
                        "lookup": {**domain_mapped,
                                   **{v: v for v in domain_mapped.values()},
                                   **{v: domain_mapped[k] for k, v in domain_non_mapped.items()}}
                    }

                    # Add integer keys as floats to accommodate incorrectly casted data.
                    for k, v in domain_mapped.items():
                        try:
                            domains[table][field]["lookup"].update({str(float(k)): v})
                        except ValueError:
                            continue

                else:
                    raise TypeError

            except (AttributeError, KeyError, TypeError, ValueError):
                yaml_paths = ", ".join(str(field_domains_path[lang]) for lang in ("en", "fr"))
                logger.exception(f"Unable to compile domains from config yamls: {yaml_paths}. Invalid schema "
                                 f"definition for table: {table}, field: {field}.")
                sys.exit(1)

    return domains


def compile_dtypes(length: bool = False) -> dict:
    """
    Compiles the dtype for each field in each NRN dataset. Optionally includes the field length.

    :param bool length: includes the length of the field in the returned data.
    :return dict: dictionary of dtypes and, optionally, length for each attribute of each NRN dataset.
    """

    dist_format = load_yaml(distribution_format_path)
    dtypes = dict()

    try:

        # Iterate tables.
        for name in dist_format:
            dtypes[name] = dict()

            # Iterate fields.
            for field, dtype in dist_format[name]["fields"].items():

                # Compile dtype and field length.
                dtypes[name][field] = dtype if length else dtype[0]

    except (AttributeError, KeyError, ValueError):
        logger.exception(f"Invalid schema definition: {dist_format}.")
        sys.exit(1)

    return dtypes


def explode_geometry(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Explodes MultiLineStrings and MultiPoints to LineStrings and Points, respectively.

    :param gpd.GeoDataFrame gdf: GeoDataFrame.
    :return gpd.GeoDataFrame: GeoDataFrame containing only single-part geometries.
    """

    logger.info("Exploding multi-type geometries.")

    multi_types = {"MultiLineString", "MultiPoint"}
    if len(set(gdf.geom_type.unique()).intersection(multi_types)):

        # Separate multi- and single-type records.
        multi = gdf.loc[gdf.geom_type.isin(multi_types)]
        single = gdf.loc[~gdf.index.isin(multi.index)]

        # Explode multi-type geometries.
        multi_exploded = multi.explode(ignore_index=True, index_parts=False)

        # Merge all records.
        merged = gpd.GeoDataFrame(pd.concat([single, multi_exploded], ignore_index=True), crs=gdf.crs)
        return merged.copy(deep=True)

    else:
        return gdf.copy(deep=True)


def export(dfs: Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]], dst: Path, driver: str = "GPKG",
           name_schemas: Union[None, dict] = None, merge_schemas: bool = False, keep_uuid: bool = True,
           outer_pbar: Union[tqdm, trange, None] = None) -> None:
    """
    Exports one or more (Geo)DataFrames as a specified OGR driver file / layer.

    :param Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]] dfs: dictionary of NRN dataset names and (Geo)DataFrames.
    :param Path dst: output path.
    :param str driver: OGR driver short name, default='GPKG'.
    :param Union[None, dict] name_schemas: optional dictionary mapping of dataset and field names for each provided
        dataset. Expected dictionary format:
        {
            <dataset_name>:
                name: <new_dataset_name>
                fields:
                    <field_name>: <new_field_name>
                    ...
            ...
        }
    :param bool merge_schemas: optional flag to merge type and name schemas such that attributes from any dataset can
        exist on each provided dataset, default False.
    :param bool keep_uuid: optional flag to preserve the uuid column, default True.
    :param Union[tqdm, trange, None] outer_pbar: optional pre-existing tqdm progress bar.
    """

    try:

        # Validate / create driver.
        driver = ogr.GetDriverByName(driver)

        # Create directory structure and data source (only create source for layer-based drivers).
        dst = Path(dst).resolve()

        if dst.suffix:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                source = driver.Open(str(dst), update=1)
            else:
                source = driver.CreateDataSource(str(dst))
        else:
            dst.mkdir(parents=True, exist_ok=True)
            source = None

        # Compile type schemas, conditionally merge.
        type_schemas = load_yaml(distribution_format_path)
        if merge_schemas:
            merged = {"spatial": any(type_schemas[table]["spatial"] for table in dfs),
                      "fields": dict(ChainMap(*[type_schema["fields"] for table, type_schema in type_schemas.items()]))}
            type_schemas = {table: merged for table in type_schemas}

        # Compile name schemas (filter datasets and fields within the existing type schemas and dataframe columns).
        if not name_schemas:
            name_schemas = {table: {"name": table, "fields": dict(zip(table_schema["fields"], table_schema["fields"]))}
                            for table, table_schema in type_schemas.items()}

        # Iterate dataframes.
        for table, df in dfs.items():

            name_schema, type_schema = name_schemas[table], type_schemas[table]
            schema = {"name": str(name_schema["name"]),
                      "spatial": type_schema["spatial"],
                      "fields": {field: {"name": name_schema["fields"][field],
                                         "type": type_schema["fields"][field][0],
                                         "width": type_schema["fields"][field][1]}
                                 for field in set(name_schema["fields"]).intersection(set(df.columns))}}

            # Conditionally add uuid to schema.
            if keep_uuid and "uuid" in df.columns:
                schema["fields"]["uuid"] = {"name": "uuid", "type": "str", "width": 32}

            # Configure layer geometry type and spatial reference system.
            spatial = schema["spatial"]
            srs = None
            geom_type = ogr.wkbNone

            if schema["spatial"]:
                srs = osr.SpatialReference()
                srs.ImportFromEPSG(df.crs.to_epsg())
                geom_type = attrgetter(f"wkb{df.geom_type.iloc[0]}")(ogr)

            # Create source (non-layer-based drivers only) and layer.
            if dst.suffix:
                layer = source.CreateLayer(name=schema["name"], srs=srs, geom_type=geom_type, options=["OVERWRITE=YES"])
            else:
                source = driver.CreateDataSource(str(dst / schema["name"]))
                layer = source.CreateLayer(name=Path(schema["name"]).stem, srs=srs, geom_type=geom_type)

            # Set field definitions from schema.
            ogr_field_map = {"float": ogr.OFTReal, "int": ogr.OFTInteger, "str": ogr.OFTString}
            for field, specs in schema["fields"].items():
                field_defn = ogr.FieldDefn(specs["name"], ogr_field_map[specs["type"]])
                field_defn.SetWidth(specs["width"])
                layer.CreateField(field_defn)

            # Reorder and rename columns to match schema.
            df = df[[*schema["fields"], "geometry"] if spatial else [*schema["fields"]]].copy(deep=True)
            df.rename(columns={field: specs["name"] for field, specs in schema["fields"].items()}, inplace=True)

            # Write layer.
            layer.StartTransaction()

            for feat in tqdm(df.itertuples(index=False), total=len(df),
                             desc=f"Writing to file={source.GetName()}, layer={table}",
                             bar_format="{desc}: |{bar}| {percentage:3.0f}% {r_bar}", leave=not bool(outer_pbar)):

                # Instantiate feature.
                feature = ogr.Feature(layer.GetLayerDefn())

                # Compile feature properties.
                properties = feat._asdict()

                # Set feature geometry, if spatial.
                if spatial:
                    geom = ogr.CreateGeometryFromWkb(properties.pop("geometry").wkb)
                    feature.SetGeometry(geom)

                # Iterate and set feature properties (attributes).
                for field_index, prop in enumerate(properties.items()):
                    feature.SetField(field_index, prop[-1])

                # Create feature.
                layer.CreateFeature(feature)

                # Clear pointer for next iteration.
                feature = None

            layer.CommitTransaction()

            # Update outer progress bar.
            if outer_pbar:
                outer_pbar.update(1)

    except FileExistsError as e:
        logger.exception(f"Invalid output directory - already exists.")
        logger.exception(e)
        sys.exit(1)
    except (KeyError, ValueError, sqlite3.Error) as e:
        logger.exception(f"Error raised when writing output: {dst}.")
        logger.exception(e)
        sys.exit(1)


def get_url(url: str, attempt: int = 1, max_attempts=10, **kwargs: dict) -> requests.Response:
    """
    Fetches a response from a url, using exponential backoff for failed attempts.

    :param str url: string url.
    :param int attempt: current count of attempts to get a response from the url.
    :param int max_attempts: maximum amount of attempts to get a response from the url.
    :param dict \*\*kwargs: keyword arguments passed to :func:`~requests.get`.
    :return requests.Response: response from the url.
    """

    logger.info(f"Fetching url request from: {url} [attempt {attempt}].")

    try:

        # Get url response.
        if attempt < max_attempts:
            response = requests.get(url, **kwargs)
        else:
            logger.exception(f"Maximum attempts reached ({max_attempts}). Unable to get URL response.")
            sys.exit(1)

    except requests.exceptions.SSLError as e:
        logger.warning("Invalid or missing SSL certificate for the provided URL. Retrying without SSL verification...")
        logger.exception(e)

        # Retry without SSL verification.
        kwargs["verify"] = False
        return get_url(url, attempt+1, **kwargs)

    except (TimeoutError, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
        # Retry with exponential backoff.
        backoff = 2 ** attempt + random.random() * 0.01
        logger.warning(f"URL request failed. Backing off for {round(backoff, 2)} seconds before retrying.")
        logger.exception(e)
        time.sleep(backoff)
        return get_url(url, attempt+1, **kwargs)

    return response


def load_gpkg(gpkg_path: Union[Path, str], find: bool = False, layers: Union[None, List[str]] = None) -> \
        Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]]:
    """
    Compiles a dictionary of NRN dataset names and associated (Geo)DataFrame from GeoPackage layers.

    :param Union[Path, str] gpkg_path: path to the GeoPackage.
    :param bool find: searches for NRN datasets in the GeoPackage based on non-exact matches with the expected dataset
        names, default False.
    :param Union[None, List[str]] layers: layer name or list of layer names to return instead of all NRN datasets.
    :return Dict[str, Union[gpd.GeoDataFrame, pd.DataFrame]]: dictionary of NRN dataset names and associated
        (Geo)DataFrames.
    """

    logger.info(f"Loading GeoPackage: {gpkg_path}.")

    dframes = dict()
    distribution_format = load_yaml(distribution_format_path)
    gpkg_path = Path(gpkg_path).resolve()

    if gpkg_path.exists():

        # Filter layers to load.
        if layers:
            distribution_format = {k: v for k, v in distribution_format.items() if k in layers}

        try:

            # Create sqlite connection.
            con = sqlite3.connect(gpkg_path)
            cur = con.cursor()

            # Load GeoPackage table names.
            gpkg_layers = list(zip(*cur.execute("select name from sqlite_master where type='table';").fetchall()))[0]

            # Create table name mapping.
            layers_map = dict()
            if find:
                for table_name in distribution_format:
                    for layer_name in gpkg_layers:
                        if layer_name.lower().find(table_name) >= 0:
                            layers_map[table_name] = layer_name
                            break
            else:
                layers_map = {name: name for name in set(distribution_format).intersection(set(gpkg_layers))}

        except sqlite3.Error:
            logger.exception(f"Unable to connect to GeoPackage: {gpkg_path}.")
            sys.exit(1)

        # Compile missing layers.
        missing_layers = set(distribution_format) - set(layers_map)
        if missing_layers:
            logger.warning(f"Missing one or more expected layers: {', '.join(map(str, sorted(missing_layers)))}. An "
                           f"exception may be raised later on if any of these layers are required.")

        # Load GeoPackage layers as (geo)dataframes.
        # Convert column names to lowercase on import.
        for table_name in layers_map:

            logger.info(f"Loading layer: {table_name}.")

            try:

                # Spatial data.
                if distribution_format[table_name]["spatial"]:
                    df = gpd.read_file(gpkg_path, layer=layers_map[table_name], driver="GPKG").rename(columns=str.lower)

                # Tabular data.
                else:
                    df = pd.read_sql_query(f"select * from {layers_map[table_name]}", con).rename(columns=str.lower)

                # Set index field: uuid.
                if "uuid" in df.columns:
                    df.index = df["uuid"]

                # Drop fid field (this field is automatically generated and not part of the NRN).
                if "fid" in df.columns:
                    df.drop(columns=["fid"], inplace=True)

                # Fill nulls with -1 (numeric fields) / "Unknown" (string fields).
                values = {field: {"float": -1, "int": -1, "str": "Unknown"}[specs[0]] for field, specs in
                          distribution_format[table_name]["fields"].items()}
                df.fillna(value=values, inplace=True)

                # Store result.
                dframes[table_name] = df.copy(deep=True)
                logger.info(f"Successfully loaded layer as dataframe: {table_name}.")

            except (fiona.errors.DriverError, pd.io.sql.DatabaseError, sqlite3.Error):
                logger.exception(f"Unable to load layer: {table_name}.")
                sys.exit(1)

    else:
        logger.exception(f"GeoPackage does not exist: {gpkg_path}.")
        sys.exit(1)

    return dframes


def load_yaml(path: Union[Path, str]) -> Any:
    """
    Loads the content of a YAML file as a Python object.

    :param Union[Path, str] path: path to the YAML file.
    :return Any: Python object consisting of the YAML content.
    """

    path = Path(path).resolve()

    with open(path, "r", encoding="utf8") as f:

        try:

            return yaml.safe_load(f)

        except (ValueError, yaml.YAMLError):
            logger.exception(f"Unable to load yaml: {path}.")


def rm_tree(path: Path) -> None:
    """
    Recursively removes a directory and all of its contents.

    :param Path path: path to the directory to be removed.
    """

    if path.exists():

        # Recursively remove directory contents.
        for child in path.iterdir():
            if child.is_file():
                child.unlink()
            else:
                rm_tree(child)

        # Remove original directory.
        path.rmdir()

    else:
        logger.exception(f"Path does not exist: \"{path}\".")
        sys.exit(1)


def round_coordinates(gdf: gpd.GeoDataFrame, precision: int = 7) -> gpd.GeoDataFrame:
    """
    Rounds the GeoDataFrame geometry coordinates to a specific decimal precision.
    Only the first 2 values (x, y) are kept for each coordinate, effectively flattening the geometry to 2-dimensions.
    Duplicated adjacent vertices are removed for LineStrings.

    :param gpd.GeoDataFrame gdf: GeoDataFrame.
    :param int precision: decimal precision to round the GeoDataFrame geometry coordinates to.
    :return gpd.GeoDataFrame: GeoDataFrame with modified decimal precision.
    """

    logger.info(f"Rounding coordinates to decimal precision: {precision}.")

    try:

        if len(gdf.geom_type.unique()) > 1:
            raise TypeError("Multiple geometry types detected for dataframe.")

        elif gdf.geom_type.iloc[0] == "LineString":
            coords = gdf["geometry"].map(lambda g: map(
                lambda pt: (round(itemgetter(0)(pt), precision), round(itemgetter(1)(pt), precision)),
                attrgetter("coords")(g))).map(tuple)

            # Remove duplicated adjacent vertices.
            flag = coords.map(set).map(len) >= 2
            coords.loc[flag] = coords.loc[flag].map(lambda g: tuple(map(itemgetter(0), groupby(g))))

            gdf["geometry"] = coords.map(LineString)

        elif gdf.geom_type.iloc[0] == "Point":
            gdf["geometry"] = gdf["geometry"].map(lambda g: attrgetter("coords")(g)[0]).map(
                lambda pt: Point([round(itemgetter(0)(pt), precision), round(itemgetter(1)(pt), precision)]))

        else:
            raise TypeError("Geometry type not supported for coordinate rounding.")

        return gdf

    except (TypeError, ValueError) as e:
        logger.exception("Unable to round coordinates for GeoDataFrame.")
        logger.exception(e)
        sys.exit(1)
