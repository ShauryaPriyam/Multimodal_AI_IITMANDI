# Flood damage mapper

Maps a user-supplied bounding box and flood date. The three results are where the flood hit, what was damaged, and which settlements lost road access to a town or hospital.

Status: module stubs only. Functions raise `NotImplementedError`.

## Layout

```
app.py                  Streamlit entry point
model.py                Segmentation model and checkpoint loading
weights/flood_model.pt  Trained weights (not committed)
pipeline/satellite.py   Sentinel-1/2 and Copernicus DEM search and download
pipeline/infer.py       Flood-mask GeoTIFF
pipeline/osm.py         Pre-event buildings, roads, bridges, places via ohsome
pipeline/damage.py      Intersection of OSM features with the flood mask
pipeline/cutoff.py      Road-graph cut-off analysis
pipeline/report.py      One-page situation report
pipeline/utils.py       Bounding box, cache paths, attributions
cache/                  Downloaded rasters and OSM extracts
tests/
```

## Setup

Python 3.11.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Place a Kuro Siwo or Sen1Floods11 checkpoint at `weights/flood_model.pt`.

## Data rules

Allowed inputs:

- Sentinel-1 and Sentinel-2
- Copernicus DEM (WorldDEM-30)
- OpenStreetMap from the ohsome API at a snapshot before the flood date (`OSM_SNAPSHOT_DATE`, default `2026-07-27`)
- Kuro Siwo and Sen1Floods11 for training only

Not inputs, even for a guess at the flood extent:

- Copernicus EMS
- UNOSAT
- OpenStreetMap edits on or after the flood date, including a live Overpass or osmnx download

Sentinel-1 before and after images must be the same relative orbit and the same pass direction, 12 calendar days apart. The bounding box and date always come from the user. No study area is built into the code.

Secrets belong in `.env`, not in source.

## Footer

Every UI footer shows these lines:

Contains modified Copernicus Sentinel data 2026.

Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.

© OpenStreetMap contributors.
