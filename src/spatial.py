import geopandas as gpd


def reports_to_geodataframe(
    df,
    x_column: str = "e",
    y_column: str = "n",
    crs: str = "EPSG:2056"
) -> gpd.GeoDataFrame:
    """
    Convert ZüriWieNeu report data into a GeoDataFrame using coordinate columns.

    The ZüriWieNeu CSV already contains a 'geometry' column in WKT format,
    but it is a plain string, not a parsed geometry. This function ignores
    it and builds a fresh shapely geometry from the numeric `e` (easting)
    and `n` (northing) columns in LV95 (EPSG:2056). The WKT column is
    dropped first so the new geometry isn't accidentally mixed with the
    string version.

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
    df_local = df.copy()

    # drop the WKT string column if present so we don't end up with two
    # 'geometry' columns or rely on silent overwrites
    if "geometry" in df_local.columns:
        df_local = df_local.drop(columns="geometry")

    gdf_reports = gpd.GeoDataFrame(
        df_local,
        geometry=gpd.points_from_xy(df_local[x_column], df_local[y_column]),
        crs=crs,
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
    # both GDFs must share the same CRS (EPSG:2056); sjoin does not reproject automatically
    assert reports_gdf.crs == quartiere_gdf.crs, (
        f"CRS mismatch: reports={reports_gdf.crs}, quartiere={quartiere_gdf.crs}"
    )

    reports_with_quartiere = gpd.sjoin(
        reports_gdf,
        quartiere_gdf[["qname", "qnr", "kname", "knr", "geometry"]],
        how="left",
        predicate="within",
    )

    return reports_with_quartiere