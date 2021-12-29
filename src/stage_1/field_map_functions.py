import logging
import numpy as np
import pandas as pd
import re
import sys
from copy import deepcopy
from operator import itemgetter
from pathlib import Path
from typing import List, Union

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
import helpers


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


# Compile domains for global access.
domains = helpers.compile_domains(mapped_lang="en")


def apply_domain(series: pd.Series, table: str, field: str, **kwargs: dict) -> pd.Series:
    """
    Calls :func:`~helpers.apply_domain` to allow it's usage as a field mapping function.

    :param pd.Series series: Series.
    :param str table: the NRN dataset containing the domain values.
    :param str field: the NRN field containing the domain values.
    :param dict \*\*kwargs: keyword arguments passed to :func:`~helpers.apply_domain`.
    :return pd.Series: Series with enforced field domain.
    """

    # Retrieve domain dict.
    try:
        kwargs["domain"] = deepcopy(domains[table][field]["lookup"])
    except KeyError:
        logger.exception(f"Domain table: \"{table}\" and / or field: \"{field}\" does not exist.")
        sys.exit(1)

    return helpers.apply_domain(series, **kwargs)


def concatenate(df: Union[pd.DataFrame, pd.Series], columns: List[str], separator: str = " ") -> pd.Series:
    """
    Concatenates all values across multiple columns into a single string, excluding Nulls, Nones, and Unknowns.

    :param Union[pd.DataFrame, pd.Series] df: DataFrame.
    :param List[str] columns: list of column names.
    :param str separator: delimiter string used to join the column values.
    :return pd.Series: Series of concatenated column values, excluding Nulls, Nones, and Unknowns.
    """

    try:

        # Unpack nested series.
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df.tolist(), columns=columns, index=df.index)

        # Validate columns.
        invalid = set(columns) - set(df.columns)
        if len(invalid):
            logger.exception(f"Invalid column(s): {', '.join(invalid)}.")

        # Concatenate values, excluding Nulls, Nones, and Unknowns.
        sep = str(separator)
        return df[columns].apply(lambda row: sep.join(map(str, filter(
            lambda val: not pd.isna(val) and val not in {"None", "Unknown"}, row))), axis=1)

    except (KeyError, ValueError):
        logger.exception(f"Unable to concatenate columns: {', '.join(columns)} by \"{separator}\".")
        sys.exit(1)


def direct(series: pd.Series, cast_type: str = None) -> pd.Series:
    """
    Returns the given series with optional dtype casting. Intended to provide a function call for direct (1:1) field
    mapping.
    Note the following pandas casting bugs and workarounds: https://github.com/pandas-dev/pandas/issues/37626.

    Possible yaml construction of direct field mapping:

    1) target_field:
         fields: source_field or raw value
         functions:
           - function: direct
             cast_type: 'int'

    2) target_field: source_field

    :param pd.Series series: Series.
    :param str cast_type: string representation of a python type class to be casted to. Must be one of: 'float', 'int',
        'str'.
    :return pd.Series: unaltered Series or Series with casted dtype.
    """

    try:

        # Return uncasted series.
        if cast_type is None:
            return series

        # Return casted series.
        elif cast_type == "float":
            return series.astype("category").astype(float)
        elif cast_type == "int":
            return series.astype("float").astype("Int64")
        elif cast_type == "str":
            return series.astype(str).replace("nan", np.nan)
        else:
            logger.exception(f"Invalid cast type \"{cast_type}\". Must be one of float, int, str.")
            sys.exit(1)

    except (TypeError, ValueError):
        logger.exception(f"Unable to cast series from {series.dtype.name} to {cast_type}.")
        sys.exit(1)


def map_values(series: pd.Series, lookup: dict, case_sensitive: bool = False) -> pd.Series:
    """
    Maps Series values based on a lookup dictionary. Non-matches retain their original value.

    :param pd.Series series: Series.
    :param dict lookup: dictionary of value mappings.
    :param bool case_sensitive: lookup keys are case sensitive, default False.
    :return pd.Series: Series with mapped values.
    """

    if case_sensitive:
        return series.map(lookup).fillna(series)

    else:
        lookup = {str(k).lower() if not isinstance(k, (float, int)) else k: v for k, v in lookup.items()}
        return series.map(
            lambda val: str(val).lower() if not isinstance(val, (float, int)) else val).map(lookup).fillna(series)


def query_assign(df: Union[pd.DataFrame, pd.Series], columns: List[str], lookup: dict, engine: str = "python",
                 **kwargs: dict) -> pd.Series:
    """
    Populates a Series based on a lookup dictionary of queries. Non-matches will be Null.

    :param Union[pd.DataFrame, pd.Series] df: DataFrame or Series.
    :param List[str] columns: list of column names, once unnested if input is a nested Series.
    :param dict lookup: dictionary of query-value mappings, where queries are stored as the dictionary keys. Each query
        maps to a dictionary containing a 'value' key and 'type' key. 'type' can be either 'column' or 'string' and
        indicates whether 'value' is to be taken as raw string or column name. If 'value' is a column name, then the
        assigned value for each record selected by the query will be from the indicated column of that record. Format:

        str (query):
            {
                'value': str
                'type': 'column' | 'string' (default)
            }

    :param str engine: the engine used to evaluate the expression (see :func:`~pd.eval`), default 'python'.
    :param dict \*\*kwargs: keyword arguments passed to :func:`~pd.DataFrame.query`.
    :return pd.Series: Series populated with values based on queries.
    """

    try:

        # Validate inputs.
        if not isinstance(columns, list):
            columns = [columns]
        columns = list(map(str.lower, columns))

        # Validate and configure assignment type (string vs. column).
        for query, output in lookup.items():

            if "type" not in output.keys():
                lookup[output]["type"] = "string"

            if output["type"] == "column":
                lookup[query]["value"] = lookup[query]["value"].lower()

                if lookup[query]["value"] not in columns:
                    logger.exception(f"Invalid column for lookup['{query}']: {lookup[query]['value']}.")

        # Unpack nested series.
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df.tolist(), columns=columns, index=df.index)

        # Configure output series.
        series = pd.Series(None, index=df.index)

        # Iterate queries.
        for query, output in lookup.items():

            # Retrieve indexes which match query.
            indexes = df.query(query, engine=engine, **kwargs).index

            # Update series with string or another dataframe column.
            if output["type"] == "string":
                series.loc[indexes] = str(output["value"])
            else:
                series.loc[indexes] = df.loc[indexes, output["value"]]

        return series

    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def regex_find(series: pd.Series, pattern: str, match_index: int, group_index: Union[int, List[int]],
               strip_result: bool = False, sub_inplace: dict = None) -> pd.Series:
    """
    Populates a Series based on the selection or removal of a regular expression match.

    :param pd.Series series: Series.
    :param str pattern: regular expression.
    :param int match_index: index of regular expression matches to be selected.
    :param Union[int, List[int]] group_index: index(es) of match group(s) to be selected within the regular expression
        matches.
    :param bool strip_result: selected match value should be stripped from the original string, default False.
    :param dict sub_inplace: keyword arguments passed to :func:`~re.sub`, default None. This allows the regular
        expression to be matched against a modification of the original string, but still return the match as it appears
        in the original string. This is useful when matching against French strings which may contain several hyphens.
        For instance, to match 'de la' in 'Chemin-de-la-Grande-Rivière', sub_inplace can call :func:`~re.sub` to replace
        '-' with ' '. If strip_result=False, then 'de la' will be returned, else 'Chemin-Grande-Rivière' will be
        returned.
    :return pd.Series: Series populated with the result of a regular expression.
    """

    def regex_find_multiple_idx(val: str, pattern: str) -> Union[str, None]:
        """
        Returns the selected or removed result of a regular expression match. Non-matches will return Null.

        :param str val: value.
        :param str pattern: regular expression.
        :return Union[str, None]: Null or the string resulting from the regular expression match. Since there are
            multiple group_index values, the first group_index with a match will be returned.
        """

        try:

            matches = re.finditer(pattern, re.sub(**sub_inplace, string=val) if sub_inplace else val, flags=re.I)
            result = [[itemgetter(*group_index)(m.groups()), m.start(), m.end()] for m in matches][match_index]
            result[0] = [grp for grp in result[0] if grp != "" and not pd.isna(grp)][0]

            # Return stripped result, if required.
            return strip(val, *result[1:]) if strip_result else itemgetter(0)(result)

        except (IndexError, ValueError):
            return val if strip_result else np.nan

    def regex_find_single_idx(val: str, pattern: str) -> Union[str, None]:
        """
        Returns the selected or removed result of a regular expression match. Non-matches will return Null.

        :param str val: value.
        :param str pattern: regular expression.
        :return Union[str, None]: Null or the string resulting from the regular expression match.
        """

        try:

            matches = re.finditer(pattern, re.sub(**sub_inplace, string=val) if sub_inplace else val, flags=re.I)
            result = [[m.groups()[group_index], m.start(), m.end()] for m in matches][match_index]

            # Return stripped result, if required.
            return strip(val, *result[1:]) if strip_result else itemgetter(0)(result)

        except (IndexError, ValueError):
            return val if strip_result else np.nan

    def strip(val: str, start: int, end: int) -> Union[str, None]:
        """
        Strips the characters between the provided index range, inclusively, from the given string.

        :param str val: value.
        :param int start: the starting index of the character range to be removed.
        :param int end: the ending index of the character range to be removed.
        :return Union[str, None]: Null or the provided string excluding the given character range.
        """

        try:

            # Reset start index to avoid stacking spaces and hyphens.
            if start > 0 and end < len(val):
                while val[start - 1] == val[end] and val[end] in {" ", "-"}:
                    start -= 1

            return "".join(map(str, [val[:start], val[end:]]))

        except (IndexError, ValueError):
            return val if strip_result else np.nan

    # Validate inputs.
    pattern = validate_regex(pattern)
    if sub_inplace:
        if {"pattern", "repl"}.issubset(set(sub_inplace.keys())):
            sub_inplace["pattern"] = validate_regex(sub_inplace["pattern"])
            sub_inplace["repl"] = validate_regex(sub_inplace["repl"])
            sub_inplace["flags"] = re.I
        else:
            logger.exception("Invalid input for sub_inplace. Missing one or more required re.sub kwargs: pattern, "
                             "repl.")
            sys.exit(1)

    # Replace empty or nan values with numpy nan.
    series.loc[(series == "") | (series.isna())] = np.nan

    # Compile valid records.
    series_valid = series.loc[~series.isna()].copy(deep=True)

    # Compile regex results, based on required group indexes.
    if isinstance(group_index, (int, np.int_)):
        results = series_valid.map(lambda val: regex_find_single_idx(str(val), pattern))
    else:
        results = series_valid.map(lambda val: regex_find_multiple_idx(str(val), pattern))

    # Strip leading and trailing whitespaces and hyphens.
    results = results.map(lambda val: str(val).strip(" -"))

    # Update series with results.
    series.loc[series_valid.index] = results

    return series


def regex_sub(series: pd.Series, **kwargs: dict) -> pd.Series:
    """
    Populates a Series based on the substitution of a regular expression match.

    :param pd.Series series: Series.
    :param dict \*\*kwargs: keyword arguments passed to :func:`~re.sub`. kwarg 'repl' can be a regular expression or
        dictionary of value mappings.
    :return pd.Series: Series populated with the result of regular expression substitution.
    """

    # Validate inputs.
    kwargs["pattern"] = validate_regex(kwargs["pattern"])
    if isinstance(kwargs["repl"], str):
        kwargs["repl"] = validate_regex(kwargs["repl"])
    elif isinstance(kwargs["repl"], dict):

        # Lowercase keys and overwrite repl with lambda function.
        lookup = {k.lower(): v for k, v in deepcopy(kwargs["repl"]).items()}
        kwargs["repl"] = lambda match: lookup[match.string[match.start(): match.end()].lower()]

    else:
        logger.exception("Invalid input. 'repl' must be a regex string or lookup dictionary.")

    # Replace empty or nan values with numpy nan.
    series.loc[(series == "") | (series.isna())] = np.nan

    # Compile valid records.
    series_valid = series.loc[~series.isna()].copy(deep=True)

    # Apply regex substitution.
    series.loc[series_valid.index] = series_valid.map(lambda val: re.sub(**kwargs, string=str(val), flags=re.I))

    return series


def validate_regex(pattern: str) -> str:
    """
    Validates a regular expression.

    :param str pattern: regular expression. Any instances of the keyword format '(domain_{table}_{field})' will be
        replaced with the domain values of the parsed table and field names, concatenated by the string '|'.
        Example: (domain_roadseg_provider) --> (Other|Federal|Provincial / Territorial|Municipal).
    :return str: validated regular expression.
    """

    try:

        # Compile regular expression.
        re.compile(pattern)

        # Substitute domain keywords with values.
        # Process: iterate keyword matches, parse the resulting keywords and use as domain lookup keys, replace the
        # original values with '|' joined domain values.
        for kw in set([itemgetter(0)(match.groups()) for match in
                       re.finditer(r"\(domain_(.*?)\)", pattern, flags=re.I)
                       ]):

            table, field = kw.split("_")
            domain = domains[table][field]["values"]

            if domain:
                pattern = pattern.replace(kw, "|".join(map(str, domain)))

        return pattern

    except re.error:
        logger.exception(f"Invalid regular expression: {pattern}.")
        sys.exit(1)
