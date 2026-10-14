"""Write a one-page situation report for one bounding box and flood date."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from pipeline.cutoff import CutoffAssessment
from pipeline.damage import DamageAssessment
from pipeline.satellite import Sentinel1Pair
from pipeline.utils import BBox


def write_situation_report(
    output_html: Path,
    bbox: BBox,
    flood_date: date,
    flood_mask: Path,
    damage: DamageAssessment,
    cutoff: CutoffAssessment,
    s1_pair: Sentinel1Pair,
    osm_snapshot: date,
) -> Path:
    """Write a one-page HTML situation report.

    Parameters
    ----------
    output_html:
        Destination HTML file.
    bbox:
        Bounding box the user supplied.
    flood_date:
        Flood date the user supplied.
    flood_mask:
        GeoTIFF from ``pipeline.infer.predict_flood_mask``.
    damage:
        Building, road, and bridge intersections.
    cutoff:
        Settlement access result.
    s1_pair:
        Sentinel-1 pair that was compared. The page records the relative
        orbit, pass direction, scene ids, dates, and the 12-day gap.
    osm_snapshot:
        ohsome timestamp actually queried. It is before ``flood_date``.

    Returns
    -------
    Path
        ``output_html``. The page answers, in order, where the flood hit,
        what was damaged, and who is cut off. Its footer contains the three
        lines in ``pipeline.utils.ATTRIBUTIONS``, unchanged.

    Raises
    ------
    PipelineError
        If ``flood_mask`` is missing or ``osm_snapshot`` is not before
        ``flood_date``.
    """
    raise NotImplementedError
