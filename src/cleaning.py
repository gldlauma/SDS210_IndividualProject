import pandas as pd

# Function: converting date columns from text to datetime format
def parse_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Convert date columns in the ZüriWieNeu dataset from text to datetime format.   
    Parameters    
    ----------    
    df : pandas.DataFrame        
        Raw ZüriWieNeu report data.    
    Returns    
    -------    
    pandas.DataFrame        
        DataFrame with parsed datetime columns.    
    '''

    df_cleaned = df.copy()

    datetime_columns = [
        "requested_datetime",
        "agency_sent_datetime",
        "updated_datetime"
    ]

    for column in datetime_columns:
        if column in df_cleaned.columns:
            df_cleaned[column] = pd.to_datetime(df_cleaned[column], format="%Y-%m-%dT%H:%M:%S")
    
    return df_cleaned


# Function: removing any existing duplicate reports based on their ID
def remove_duplicate_reports(
    df: pd.DataFrame,
    id_column: str = "service_request_id"
) -> pd.DataFrame:
    """
    Remove duplicate reports from the ZüriWieNeu dataset based on the unique
    service request ID.

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


# Function: converting date columns from text to datetime format
def add_time_columns(df: pd.DataFrame, date_column: str = "requested_datetime") -> pd.DataFrame:
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


# create only one big function for cleaning the dataset
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
    3. Add year, month, and year_month columns for time-based analysis.
    """

    df_cleaned = parse_datetime_columns(df)
    df_cleaned = remove_duplicate_reports(df_cleaned)
    df_cleaned = add_time_columns(df_cleaned)

    return df_cleaned

