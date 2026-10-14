"""Shared types, cache paths, and attribution text.

No analysis lives here. Functions are stubs until the pipeline is implemented.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path


class PipelineError(Exception):
    """Raised when a request cannot be completed without breaking the data rules."""


@dataclass(frozen=True)
class BBox:
    """WGS84 bounding box. Any place and any flood date are valid inputs.

    Attributes
    ----------
    west:
        Minimum longitude in degrees.
    south:
        Minimum latitude in degrees.
    east:
        Maximum longitude in degrees.
    north:
        Maximum latitude in degrees.
    """

    west: float
    south: float
    east: float
    north: float


ATTRIBUTIONS: tuple[str, str, str] = (
    "Contains modified Copernicus Sentinel data 2026.",
    "Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.",
    "© OpenStreetMap contributors.",
)
"""Lines that every UI footer must show, in this order."""


def cache_dir() -> Path:
    """Return the root directory for downloaded rasters and OSM extracts.

    Returns
    -------
    Path
        The ``cache/`` directory. Callers write Sentinel, DEM, and ohsome
        responses here and nowhere else.
    """
    raise NotImplementedError


def cache_path(namespace: str, key: str, suffix: str) -> Path:
    """Return a cache file path for one download.

    Parameters
    ----------
    namespace:
        Subfolder such as ``sentinel1``, ``sentinel2``, ``dem``, or ``osm``.
    key:
        Stable identifier for the request. Scene ids and ohsome query
        bodies are suitable. Signed URLs are not, because they expire.
    suffix:
        File suffix including the dot, for example ``.tif`` or ``.geojson``.

    Returns
    -------
    Path
        Path under ``cache/``. The file does not have to exist yet.
    """
    raise NotImplementedError


def configured_osm_snapshot() -> date:
    """Read the preferred pre-event OSM snapshot from the environment.

    Returns
    -------
    date
        Value of ``OSM_SNAPSHOT_DATE`` in ``.env``. The audited default for
        this project is 2026-07-27. ``pipeline.osm.resolve_snapshot`` must
        still move it earlier when that day is not before the flood date.
    """
    raise NotImplementedError
