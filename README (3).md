# FloodWatch – mapping flood damage from space

Multimodal AI Hackathon 2026, Track B: Mapping Flood Damage from Space.
Case study: the 26 August 2026 Trishuli flood, Nepal.

This is an educational prototype. It is not an operational tool, and its results are not field-verified.

## What it does

Give it an area (bounding box) and a flood date. It answers three questions:

1. **Where did the flood hit?** Compares Sentinel-1 radar images from before and after the event (same orbit track, 12 days apart) and maps debris- or water-affected areas. Sentinel-2 is used only when the sky is clear enough.
2. **What was damaged?** Takes buildings, roads and bridges from OpenStreetMap as they were before the event (ohsome API snapshot) and counts the ones that overlap the flood mask.
3. **Who is cut off?** Builds a road graph, removes flooded road segments, and lists settlements that can no longer reach the nearest hospital (or town, if one exists in OSM).

Bonus: given an upstream point, it traces the flood path down the valley using the Copernicus DEM and lists the settlements along it.

**AI component: situation-report copilot.** A language model writes a short situation report in English and Nepali and answers questions. It only receives a JSON file of numbers (`facts.json`) computed from the maps. Every number in its answer is checked against that file. If the answer contains a number that is not in the file, it is rewritten, and if it still fails the system falls back to a fixed template.

## Outputs

| File | Content |
|---|---|
| `dashboard.html` | Interactive map: flood mask, hit buildings/roads/bridges, cut-off settlements, flood path |
| `situation_report.html` | One-page report in English and Nepali |
| `facts.json` | All numbers used by the report and the copilot |
| `flood.geojson` | Flood mask polygons |

## How to run (Google Colab)

1. Open `floodwatch.ipynb` in Google Colab.
2. Register for free at https://dataspace.copernicus.eu and create an OAuth client (Sentinel Hub). You get a client ID and a client secret.
3. Get a free API key from https://console.groq.com (used for the copilot).
4. In Colab, open the key icon (Secrets) in the left sidebar and add:
   - `CDSE_ID`
   - `CDSE_SECRET`
   - `GROQ_API_KEY`
   Turn on notebook access for each one. Never paste keys into the notebook cells.
5. Set the area and date in the `CONFIG` cell:
   - `bbox` = (west, south, east, north) in degrees
   - `flood_date` = day of the event, `YYYY-MM-DD`
   - `osm_date` = OSM snapshot date. It must be before `flood_date`. The code stops with an error if it is not.
6. Run all cells. `RESULT = run()` does the full pipeline from raw satellite data, and the last cells display the dashboard and save the output files.

Requirements are installed by the first cell: `rasterio geopandas shapely pyproj networkx scipy folium requests anthropic`. Python 3.10 or newer.

## Data rules

- Inputs used: Sentinel-1, Sentinel-2, Copernicus DEM, OpenStreetMap snapshot from before the event (27 July 2026).
- Copernicus EMS (EMSR927) is used **only** in the final evaluation cell, to check results after they are produced. It is never an input to the pipeline. The EMSR927 files are not included in this repository.
- No model was trained, so no training dataset is used. (Kuro Siwo and Sen1Floods11 are not used.)

## Known problems

See the Limitations section of `REPORT.pdf`. The most important ones:

- The detected flood area in the case study is much smaller than the EMSR927 reference. See the report for the numbers.
- Results depend strongly on the detection thresholds.
- OpenStreetMap is incomplete in remote valleys, so cut-off results depend on very few road segments.
- Satellites revisit every few days, so there is no early warning.

## Attribution

- Contains modified Copernicus Sentinel data 2026.
- Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.
- © OpenStreetMap contributors (ODbL).
- Reference maps used for checking only: European Union, Copernicus Emergency Management Service data (EMSR927).
- Basemap tiles: © CARTO, © OpenStreetMap contributors.

## Team

[Full names of all team members]
