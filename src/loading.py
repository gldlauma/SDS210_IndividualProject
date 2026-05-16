import pandas as pd


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Load ZüriWieNeu report data from a local CSV file.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Raw ZüriWieNeu data as a pandas DataFrame.
    """
    # encoding="utf-8-sig" strips the BOM at the start of the file; without it,
    # the first column name would silently be "\ufeffobjectid" on some readers.
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    return df