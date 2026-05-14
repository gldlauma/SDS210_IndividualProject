import requests
import time
import pandas as pd
import geopandas as gpd
from pathlib import Path
from datetime import datetime, timedelta

def fetch_zueriwieneu_api(start_date, end_date, sleep_seconds=0.5):
    """
    Fetch ZüriWieNeu reports from the Open311 Web API.

    The Open311 endpoint caps the number of records returned per request,
    so the time range is split into one-month windows. Reports from all
    windows are combined into a single DataFrame. A short pause between
    requests respects the server's rate limit.

    The API wraps the list of reports under a top-level key called
    "service_requests". This function unwraps that structure before
    returning, so the caller receives a flat DataFrame of reports.

    Parameters
    ----------
    start_date : str
        Start of the time range as an ISO date string, e.g. "2013-01-01".
    end_date : str
        End of the time range as an ISO date string, e.g. "2025-12-31".
    sleep_seconds : float
        Seconds to pause between API requests (default 0.5).

    Returns
    -------
    pandas.DataFrame
        ZüriWieNeu reports with WGS84 coordinates in 'lat' and 'long'.
    """
    api_url = "https://www.zueriwieneu.ch/open311/v2/requests.json"
    all_reports = []

    current = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    while current < end:
        # Advance one calendar month at a time
        next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        window_end = min(next_month, end)

        parameters = {
            "jurisdiction_id": "zurich",
            "start_date": current.strftime("%Y-%m-%dT00:00:00+01:00"),
            "end_date":   window_end.strftime("%Y-%m-%dT00:00:00+01:00")
        }

        response = requests.get(api_url, params=parameters)

        if response.status_code == 200:
            # The Open311 API wraps the list under "service_requests"
            payload = response.json()
            chunk = payload.get("service_requests", []) if isinstance(payload, dict) else []
            all_reports.extend(chunk)
            print(f"  {current.date()} → {window_end.date()}: {len(chunk):>4d} reports")
        else:
            print(f"  Request failed for {current.date()}: status {response.status_code}")

        # Respect the API's rate limit
        time.sleep(sleep_seconds)
        current = window_end

    return pd.DataFrame(all_reports)


def reproject_to_lv95(df, lat_col="lat", long_col="long"):
    """
    Reproject WGS84 coordinates to Swiss CH1903+ / LV95.

    Adds 'e' (easting) and 'n' (northing) columns to the DataFrame so
    the API output has the same coordinate schema as the official
    CSV export from Open Data Zürich.

    Parameters
    ----------
    df : pandas.DataFrame
        Reports with WGS84 latitude and longitude columns.
    lat_col, long_col : str
        Names of the latitude and longitude columns.

    Returns
    -------
    pandas.DataFrame
        Reports with added 'e' and 'n' columns in metres (EPSG:2056).
    """
    df = df.copy()

    # The API returns coordinates as strings; convert to float first
    df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
    df[long_col] = pd.to_numeric(df[long_col], errors="coerce")

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[long_col], df[lat_col]),
        crs="EPSG:4326",
    ).to_crs("EPSG:2056")

    df["e"] = gdf.geometry.x
    df["n"] = gdf.geometry.y

    return df


def load_zueriwieneu(
    start_date="2013-01-01",
    end_date=None,
    cache_path="../data/processed/zueriwieneu_api_cache.csv",
    refresh=False,
):
    """
    Load ZüriWieNeu reports from the Open311 API with local caching.

    On the first run, or when refresh=True, the data is fetched from the
    API, reprojected from WGS84 to Swiss LV95, and saved to disk as a CSV.
    On subsequent runs the cached file is loaded directly, which keeps
    the notebook fast and reproducible.

    Parameters
    ----------
    start_date : str
        Start of the time range as an ISO date string.
    end_date : str or None
        End of the time range. If None, today's date is used.
    cache_path : str or pathlib.Path
        Location of the local CSV cache.
    refresh : bool
        If True, ignore the cache and re-fetch from the API.

    Returns
    -------
    pandas.DataFrame
        Raw ZüriWieNeu report data with 'e' and 'n' columns in LV95,
        ready for cleaning.
    """
    cache_path = Path(cache_path)

    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    if cache_path.exists() and not refresh:
        print(f"Loading from cache: {cache_path}")
        return pd.read_csv(cache_path)

    print(f"Fetching from Open311 API: {start_date} to {end_date}")
    df = fetch_zueriwieneu_api(start_date, end_date)

    # Reproject WGS84 → LV95 so the API data matches the CSV schema
    df = reproject_to_lv95(df)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_path, index=False)
    print(f"Cached {len(df):,} reports to {cache_path}")

    return df