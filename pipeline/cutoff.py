"""Find settlements that lose road access to a town or hospital.

The road geometries come from the pre-event ohsome snapshot. A live OSM
download, including one made through osmnx, must not replace that snapshot.
osmnx and networkx are used only to operate on the snapshot graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd


@dataclass(frozen=True)
class CutoffAssessment:
    """Road access before and after flooded roads are removed.

    Attributes
    ----------
    settlements:
        One row per settlement. ``status`` is one of ``cut_off``,
        ``connected``, ``previously_isolated``, ``no_road_nearby``, or
        ``destination``. Distance columns, in kilometres, are
        ``distance_before_km`` and ``distance_after_km``.
    cutoff_count:
        Settlements that could reach a town or hospital before the flood
        and cannot after flooded edges are removed.
    connected_count:
        Settlements that can still reach a town or hospital.
    previously_isolated_count:
        Settlements that already had no path to a town or hospital before
        any flooded edge was removed.
    """

    settlements: gpd.GeoDataFrame
    cutoff_count: int
    connected_count: int
    previously_isolated_count: int


def analyze_cutoff(
    roads: gpd.GeoDataFrame,
    flood_mask: Path,
    settlements: gpd.GeoDataFrame,
    destinations: gpd.GeoDataFrame,
) -> CutoffAssessment:
    """Report settlements with no remaining road path to a town or hospital.

    Parameters
    ----------
    roads:
        Pre-event driveable roads from ``pipeline.osm.fetch_roads``.
    flood_mask:
        GeoTIFF from ``pipeline.infer.predict_flood_mask``. Road pieces
        that intersect pixels with value 1 are treated as impassable.
    settlements:
        Pre-event places from ``pipeline.osm.fetch_settlements``.
    destinations:
        Pre-event towns and hospitals from ``pipeline.osm.fetch_destinations``.
        A settlement is cut off only when every path to every destination
        is broken, and at least one path existed before the flood.

    Returns
    -------
    CutoffAssessment
        Status of each settlement on the pre-event road graph. Places that
        were already disconnected are not counted as cut off by the flood.
        Places farther than the snap distance from any road are
        ``no_road_nearby``. Towns and hospitals are ``destination``.

    Raises
    ------
    PipelineError
        If ``flood_mask`` cannot be read. Missing roads or places are an
        empty assessment, not an error.
    """
    raise NotImplementedError
