"""Search and download Sentinel-1, Sentinel-2, and Copernicus DEM.

Allowed inputs are Sentinel-1, Sentinel-2, and Copernicus WorldDEM-30
(Copernicus DEM GLO-30). Copernicus EMS and UNOSAT are not inputs.
Nothing in this module is specific to one flood or one bounding box.

Sentinel-1 change detection must compare two acquisitions on the same
relative orbit and the same pass direction, exactly 12 calendar days apart.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from pipeline.utils import BBox


@dataclass(frozen=True)
class RasterScene:
    """One downloadable raster item.

    Attributes
    ----------
    item_id:
        Provider item id.
    collection:
        STAC collection name.
    acquired:
        Acquisition date. ``None`` for a DEM tile.
    hrefs:
        Asset name mapped to an unsigned URL.
    relative_orbit:
        Sentinel-1 relative orbit number. ``None`` for Sentinel-2 and DEM.
    orbit_state:
        ``ascending`` or ``descending`` for Sentinel-1. ``None`` otherwise.
    platform:
        Satellite platform name, when the provider reports one.
    """

    item_id: str
    collection: str
    acquired: date | None
    hrefs: dict[str, str]
    relative_orbit: int | None = None
    orbit_state: str | None = None
    platform: str | None = None


@dataclass(frozen=True)
class Sentinel1Pair:
    """Pre and post Sentinel-1 acquisitions on one orbit track.

    Attributes
    ----------
    pre:
        Tiles acquired before the flood date. Several tiles may be needed
        to cover the bounding box, but they must be the same pass.
    post:
        Tiles acquired on or after the flood date, from that same pass
        one repeat cycle later.
    relative_orbit:
        Relative orbit shared by ``pre`` and ``post``.
    orbit_state:
        Pass direction shared by ``pre`` and ``post``.
    delta_days:
        Calendar days from the pre date to the post date. This is 12.
    """

    pre: tuple[RasterScene, ...]
    post: tuple[RasterScene, ...]
    relative_orbit: int
    orbit_state: str
    delta_days: int


def search_sentinel1_pair(bbox: BBox, flood_date: date) -> Sentinel1Pair:
    """Find a Sentinel-1 pair on one orbit track, 12 days apart.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    flood_date:
        Flood date. The pre acquisition must fall before this date and the
        post acquisition on or after it.

    Returns
    -------
    Sentinel1Pair
        Scenes that share ``relative_orbit`` and ``orbit_state``, with
        ``delta_days`` equal to 12. A 6-day or 24-day gap, or a pair from
        two different relative orbits, is not a valid result.

    Raises
    ------
    PipelineError
        If no same-orbit 12-day pair straddles ``flood_date`` and covers
        ``bbox``. The search must not substitute a different track.
    """
    raise NotImplementedError


def search_sentinel2(
    bbox: BBox, flood_date: date
) -> tuple[RasterScene | None, RasterScene | None]:
    """Find pre-flood and post-flood Sentinel-2 L2A scenes.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.
    flood_date:
        Flood date. The first scene must be before this date and the
        second on or after it.

    Returns
    -------
    tuple[RasterScene | None, RasterScene | None]
        ``(pre, post)``. Either side is ``None`` when cloud cover leaves
        no usable scene. Sentinel-2 is not required to share an orbit or
        a 12-day gap. That constraint applies only to Sentinel-1.
    """
    raise NotImplementedError


def search_copernicus_dem(bbox: BBox) -> list[RasterScene]:
    """Find Copernicus DEM GLO-30 tiles covering the bounding box.

    Parameters
    ----------
    bbox:
        West, south, east, north in WGS84 degrees.

    Returns
    -------
    list[RasterScene]
        WorldDEM-30 tiles whose footprint intersects ``bbox``. This is the
        DEM the map is produced from, which is why the UI carries the
        Copernicus WorldDEM-30 attribution.

    Raises
    ------
    PipelineError
        If no Copernicus DEM tile covers ``bbox``.
    """
    raise NotImplementedError


def download_rasters(
    bbox: BBox,
    s1_pair: Sentinel1Pair,
    s2_pre: RasterScene | None,
    s2_post: RasterScene | None,
    dem_tiles: list[RasterScene],
) -> dict[str, Path]:
    """Download the selected rasters into ``cache/``.

    Parameters
    ----------
    bbox:
        Window to read from each scene. Full scenes are not stored when a
        windowed read is enough.
    s1_pair:
        Same-orbit Sentinel-1 pair from ``search_sentinel1_pair``.
    s2_pre:
        Pre-flood Sentinel-2 scene, or ``None``.
    s2_post:
        Post-flood Sentinel-2 scene, or ``None``.
    dem_tiles:
        Copernicus DEM tiles from ``search_copernicus_dem``.

    Returns
    -------
    dict[str, Path]
        Local GeoTIFF paths. Required keys are ``vv_pre``, ``vv_post``,
        and ``dem``. Optional keys are ``vh_pre``, ``vh_post``, ``s2_pre``,
        and ``s2_post``.

    Raises
    ------
    PipelineError
        If a required asset cannot be read, or if a URL points at
        Copernicus EMS or UNOSAT.
    """
    raise NotImplementedError
