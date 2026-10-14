"""Skeleton checks: modules import, stubs are unimplemented, attributions match."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

import app
import model
import pipeline
from pipeline import cutoff, damage, infer, osm, report, satellite, utils
from pipeline.satellite import RasterScene, Sentinel1Pair
from pipeline.utils import ATTRIBUTIONS, BBox


def test_package_imports() -> None:
    assert pipeline.satellite is satellite
    assert callable(app.main)
    assert callable(model.load_weights)


def test_attributions_are_exact() -> None:
    assert ATTRIBUTIONS == (
        "Contains modified Copernicus Sentinel data 2026.",
        "Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.",
        "© OpenStreetMap contributors.",
    )


def test_stubs_raise() -> None:
    bbox = BBox(west=0.0, south=0.0, east=1.0, north=1.0)
    flood_date = date(2024, 6, 1)
    scene = RasterScene(
        item_id="scene",
        collection="sentinel-1-rtc",
        acquired=flood_date,
        hrefs={},
        relative_orbit=1,
        orbit_state="ascending",
    )
    pair = Sentinel1Pair(
        pre=(scene,),
        post=(scene,),
        relative_orbit=1,
        orbit_state="ascending",
        delta_days=12,
    )
    mask = Path("mask.tif")
    weights = Path("weights/flood_model.pt")

    with pytest.raises(NotImplementedError):
        satellite.search_sentinel1_pair(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        satellite.search_sentinel2(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        satellite.search_copernicus_dem(bbox)
    with pytest.raises(NotImplementedError):
        satellite.download_rasters(bbox, pair, None, None, [])
    with pytest.raises(NotImplementedError):
        infer.predict_flood_mask({}, weights, mask)
    with pytest.raises(NotImplementedError):
        osm.resolve_snapshot(flood_date, flood_date)
    with pytest.raises(NotImplementedError):
        osm.fetch_buildings(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        osm.fetch_roads(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        osm.fetch_bridges(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        osm.fetch_settlements(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        osm.fetch_destinations(bbox, flood_date)
    with pytest.raises(NotImplementedError):
        damage.assess_damage(mask, None, None, None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        cutoff.analyze_cutoff(None, mask, None, None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        report.write_situation_report(
            Path("report.html"),
            bbox,
            flood_date,
            mask,
            None,  # type: ignore[arg-type]
            None,  # type: ignore[arg-type]
            pair,
            flood_date,
        )
    with pytest.raises(NotImplementedError):
        utils.cache_dir()
    with pytest.raises(NotImplementedError):
        utils.cache_path("osm", "key", ".geojson")
    with pytest.raises(NotImplementedError):
        utils.configured_osm_snapshot()
    with pytest.raises(NotImplementedError):
        model.load_weights(weights)
    with pytest.raises(NotImplementedError):
        model.FloodModel()
    with pytest.raises(NotImplementedError):
        app.main()
