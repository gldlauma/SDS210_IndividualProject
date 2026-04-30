import pandas as pd


def count_reports_by_year(
    df: pd.DataFrame,
    year_column: str = "year"
) -> pd.DataFrame:
    """
    Count the number of ZüriWieNeu reports per year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned ZüriWieNeu report data.
    year_column : str, default "year"
        Column containing the year of each report.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per year and the corresponding number of reports.

    Output Columns
    --------------
    year : int
        Calendar year.
    report_count : int
        Number of reports submitted in that year.
    """

    yearly_counts = (
        df
        .groupby(year_column)
        .size()
        .reset_index(name="report_count")
        .sort_values(year_column)
    )

    return yearly_counts


def count_reports_by_month(
    df: pd.DataFrame,
    month_column: str = "year_month"
) -> pd.DataFrame:
    """
    Count the number of ZüriWieNeu reports per month.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned ZüriWieNeu report data.
    month_column : str, default "year_month"
        Column containing the month of each report as a datetime value.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per month and the corresponding number of reports.

    Output Columns
    --------------
    year_month : datetime64
        Month of the reports, represented by the first day of that month.
    report_count : int
        Number of reports submitted in that month.
    """

    monthly_counts = (
        df
        .groupby(month_column)
        .size()
        .reset_index(name="report_count")
        .sort_values(month_column)
    )

    return monthly_counts


def count_reports_by_year_and_category(
    df: pd.DataFrame,
    year_column: str = "year",
    category_column: str = "service_name"
) -> pd.DataFrame:
    """
    Count the number of ZüriWieNeu reports per year and category.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned ZüriWieNeu report data.
    year_column : str, default "year"
        Column containing the year of each report.
    category_column : str, default "service_name"
        Column containing the report category.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per year and category combination.

    Output Columns
    --------------
    year : int
        Calendar year.
    service_name : str
        Report category.
    report_count : int
        Number of reports in that year and category.
    """

    category_counts = (
        df
        .groupby([year_column, category_column])
        .size()
        .reset_index(name="report_count")
        .sort_values([year_column, category_column])
    )

    return category_counts
