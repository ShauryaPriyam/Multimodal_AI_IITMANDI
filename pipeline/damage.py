"""Intersect pre-event OpenStreetMap features with the flood mask."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd


@dataclass(frozen=True)
class DamageAssessment:
    """Features the flood mask reaches.

    Attributes
    ----------
    buildings:
        Building polygons that intersect the mask, with ``area_m2``.
    roads:
        Road lines inside the mask, with ``length_m``.
    bridges:
        Bridges that intersect the mask, with ``length_m`` or ``area_m2``
        depending on geometry type.
    building_count:
        Number of distinct buildings represented in ``buildings``.
    road_km:
        Total flooded road length in kilometres.
    bridge_count:
        Number of distinct bridges represented in ``bridges``.
    """

    buildings: gpd.GeoDataFrame
    roads: gpd.GeoDataFrame
    bridges: gpd.GeoDataFrame
    building_count: int
    road_km: float
    bridge_count: int


def assess_damage(
    flood_mask: Path,
    buildings: gpd.GeoDataFrame,
    roads: gpd.GeoDataFrame,
    bridges: gpd.GeoDataFrame,
) -> DamageAssessment:
    """Measure buildings, roads, and bridges that intersect the flood mask.

    Parameters
    ----------
    flood_mask:
        GeoTIFF written by ``pipeline.infer.predict_flood_mask``. Only
        pixels with value 1 count as flood.
    buildings:
        Pre-event building polygons from ``pipeline.osm.fetch_buildings``.
    roads:
        Pre-event roads from ``pipeline.osm.fetch_roads``.
    bridges:
        Pre-event bridges from ``pipeline.osm.fetch_bridges``.

    Returns
    -------
    DamageAssessment
        Intersections and the three summary counts. Lengths and areas are
        computed in a local projected CRS. An empty input layer produces
        an empty result and a zero count, which is a valid outcome.

    Raises
    ------
    PipelineError
        If ``flood_mask`` is missing or is not a readable single-band raster.
    """
    raise NotImplementedError
