import pandas as pd


def parse_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns in the ZüriWieNeu dataset from text to datetime format.

    The CSV timestamps are naive ISO 8601 strings in Zurich local time
    (e.g. "2024-01-07T23:32:05"). The downstream analysis only uses the
    year and month, so the timestamps are kept as naive datetimes — no
    UTC conversion is applied. Any malformed timestamp becomes NaT.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw ZüriWieNeu report data, which has been loaded through the
        "load_csv_data" function in the loading.py script.

    Returns
    -------
    pandas.DataFrame
        DataFrame with parsed datetime columns.
    """
    df_cleaned = df.copy()

    datetime_columns = [
        "requested_datetime",
        "agency_sent_datetime",
        "updated_datetime",
    ]

    for column in datetime_columns:
        if column in df_cleaned.columns:
            df_cleaned[column] = pd.to_datetime(
                df_cleaned[column],
                format="ISO8601",
                errors="coerce",
            )

    return df_cleaned


def remove_duplicate_reports(
    df: pd.DataFrame,
    id_column: str = "service_request_id"
) -> pd.DataFrame:
    """
    Remove duplicate reports from the ZüriWieNeu dataset based on the unique
    service request ID.

    Note
    ----
    On the current CSV export this function finds 0 duplicates —
    service_request_id is already unique. It is kept as a defensive step
    in case a future export contains duplicates (for example after
    merging two snapshots).

    Parameters
    ----------
    df : pandas.DataFrame
        ZüriWieNeu report data.
    id_column : str, default "service_request_id"
        Column containing the unique report identifier.

    Returns
    -------
    pandas.DataFrame
        DataFrame with duplicate reports removed.
    """
    df_cleaned = df.copy()

    if id_column in df_cleaned.columns:
        df_cleaned = df_cleaned.drop_duplicates(subset=id_column)

    return df_cleaned


def drop_redundant_service_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop the service_code column if it is identical to service_name.

    The ZüriWieNeu export contains both 'service_code' and 'service_name'.
    In the current export they hold identical values for every row, so
    'service_code' is redundant. This function drops it if (and only if)
    that identity holds; otherwise it returns the DataFrame unchanged so
    no information is lost silently.

    Parameters
    ----------
    df : pandas.DataFrame
        ZüriWieNeu report data.

    Returns
    -------
    pandas.DataFrame
        DataFrame with service_code removed if it duplicated service_name.
    """
    df_cleaned = df.copy()

    if (
        "service_code" in df_cleaned.columns
        and "service_name" in df_cleaned.columns
        and (df_cleaned["service_code"] == df_cleaned["service_name"]).all()
    ):
        df_cleaned = df_cleaned.drop(columns="service_code")

    return df_cleaned


def add_time_columns(
    df: pd.DataFrame,
    date_column: str = "requested_datetime"
) -> pd.DataFrame:
    """
    Add time-based columns for temporal analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        ZüriWieNeu report data.
    date_column : str, default "requested_datetime"
        Column containing the date and time when a report was submitted.

    Returns
    -------
    pandas.DataFrame
        DataFrame with additional columns for year, month, and year-month.

    Added Columns
    -------------
    year : int
        Year in which the report was submitted.
    month : int
        Month in which the report was submitted.
    year_month : datetime64
        First day of the corresponding month, useful for monthly time series plots.
    """
    df_cleaned = df.copy()

    if date_column in df_cleaned.columns:
        df_cleaned["year"] = df_cleaned[date_column].dt.year
        df_cleaned["month"] = df_cleaned[date_column].dt.month
        df_cleaned["year_month"] = (
            df_cleaned[date_column]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

    return df_cleaned


def clean_reports(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full cleaning workflow for the ZüriWieNeu dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw ZüriWieNeu report data.

    Returns
    -------
    pandas.DataFrame
        Cleaned report data ready for temporal analysis.

    Cleaning Steps
    --------------
    1. Convert datetime columns from text to datetime format.
    2. Remove duplicate reports based on service_request_id.
    3. Drop service_code if it is identical to service_name.
    4. Add year, month, and year_month columns for time-based analysis.
    """
    # We intentionally keep all source columns through cleaning rather than
    # slimming the DataFrame here, so that later notebooks can use any field
    # (e.g. status, interface_used) without re-loading the raw CSV.

    df_cleaned = parse_datetime_columns(df)              # step 1: timestamps → naive datetime
    df_cleaned = remove_duplicate_reports(df_cleaned)    # step 2: drop duplicate service_request_ids
    df_cleaned = drop_redundant_service_code(df_cleaned) # step 3: drop service_code if == service_name
    df_cleaned = add_time_columns(df_cleaned)            # step 4: derive year / month / year_month

    return df_cleaned