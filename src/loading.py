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
    df = pd.read_csv(file_path)
    return df
