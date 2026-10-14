"""Download pre-event OpenStreetMap features from the ohsome API.

Current Overpass extracts and OSM edits made on or after the flood date
are not allowed. Copernicus EMS and UNOSAT are not used to choose features.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from pipeline.utils import BBox

if TYPE_CHECKING:
    import geopandas as gpd


def resolve_snapshot(flood_date: date, configured: date | None = None) -> date:
    """Choose an ohsome timestamp that is strictly before the flood.

    Parameters
    ----------
    flood_date:
        Flood date supplied with the bounding box.
    configured:
        Preferred snapshot, normally ``OSM_SNAPSHOT_DATE`` from ``.env``
        (2026-07-27 unless the environment overrides it). When ``None``,
        the configured environment value is used.

    Returns
    -------
    date
        A calendar day earlier than ``flood_date``. If ``configured`` is
        already before the flood, it is kept. Otherwise the snapshot moves
        to the day before the flood so post-event edits cannot be read.

    Raises
    ------
    PipelineError
        If the resulting day is not before ``flood_date``.
    """
    raise NotImplementedError


def fetch_buildings(bbox: BBox, snapshot: date) -> gpd.GeoDataFrame:
    """Download building footprints at the pre-event snapshot.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    snapshot:
        ohsome time from ``resolve_snapshot``. Must be before the flood date.

    Returns
    -------
    geopandas.GeoDataFrame
        Polygon buildings in EPSG:4326, including OSM id, ``name``, and
        ``building`` when those tags exist. Empty when the snapshot has no
        buildings. The response is cached under ``cache/osm/``.
    """
    raise NotImplementedError


def fetch_roads(bbox: BBox, snapshot: date) -> gpd.GeoDataFrame:
    """Download driveable roads at the pre-event snapshot.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    snapshot:
        ohsome time from ``resolve_snapshot``. Must be before the flood date.

    Returns
    -------
    geopandas.GeoDataFrame
        Line geometries in EPSG:4326 for roads a vehicle can use, including
        OSM id, ``name``, ``highway``, and bridge tags. Footways, paths, and
        cycleways are excluded. Empty when the snapshot has no such roads.
        Cached under ``cache/osm/``.
    """
    raise NotImplementedError


def fetch_bridges(bbox: BBox, snapshot: date) -> gpd.GeoDataFrame:
    """Download bridges at the pre-event snapshot.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    snapshot:
        ohsome time from ``resolve_snapshot``. Must be before the flood date.

    Returns
    -------
    geopandas.GeoDataFrame
        Bridge lines or polygons in EPSG:4326 (``bridge=yes`` or
        ``man_made=bridge``), with OSM id and ``name``. Empty when the
        snapshot has no bridges. Cached under ``cache/osm/``.
    """
    raise NotImplementedError


def fetch_settlements(bbox: BBox, snapshot: date) -> gpd.GeoDataFrame:
    """Download settlements at the pre-event snapshot.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    snapshot:
        ohsome time from ``resolve_snapshot``. Must be before the flood date.

    Returns
    -------
    geopandas.GeoDataFrame
        Points in EPSG:4326 for ``place`` city, town, village, and hamlet,
        with OSM id, ``name``, and ``place``. Empty when none exist.
        Cached under ``cache/osm/``.
    """
    raise NotImplementedError


def fetch_destinations(bbox: BBox, snapshot: date) -> gpd.GeoDataFrame:
    """Download towns and hospitals used as road-access destinations.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    snapshot:
        ohsome time from ``resolve_snapshot``. Must be before the flood date.

    Returns
    -------
    geopandas.GeoDataFrame
        Points in EPSG:4326 for ``place`` city or town, and for ``amenity``
        hospital or clinic. Columns include OSM id, ``name``, and a
        ``destination_kind`` of ``town`` or ``hospital``. Empty when none
        exist. Cached under ``cache/osm/``.
    """
    raise NotImplementedError
