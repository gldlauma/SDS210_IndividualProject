import geopandas as gpd


def reports_to_geodataframe(
    df,
    x_column: str = "e",
    y_column: str = "n",
    crs: str = "EPSG:2056"
) -> gpd.GeoDataFrame:
    """
    Convert ZüriWieNeu report data into a GeoDataFrame using coordinate columns.

    Parameters
    ----------
    df : pandas.DataFrame
        ZüriWieNeu report data containing coordinate columns.
    x_column : str, default "e"
        Column containing the east coordinate.
    y_column : str, default "n"
        Column containing the north coordinate.
    crs : str, default "EPSG:2056"
        Coordinate reference system of the input coordinates.

    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame with point geometries for each report.
    """

    gdf_reports = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[x_column], df[y_column]),
        crs=crs
    )

    return gdf_reports


def join_reports_to_quartiere(
    reports_gdf: gpd.GeoDataFrame,
    quartiere_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Spatially join ZüriWieNeu report points to Zurich Quartier polygons.

    Parameters
    ----------
    reports_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing report point geometries.
    quartiere_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing Zurich Quartier polygon geometries.

    Returns
    -------
    geopandas.GeoDataFrame
        Report GeoDataFrame with additional Quartier attributes such as
        qname, qnr, kname, and knr.
    """

    reports_with_quartiere = gpd.sjoin(
        reports_gdf,
        quartiere_gdf[["qname", "qnr", "kname", "knr", "geometry"]],
        how="left",
        predicate="within"
    )

    return reports_with_quartiere
