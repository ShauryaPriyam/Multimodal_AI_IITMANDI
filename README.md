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
| `index.html` | Viewer wrapper with Map, Report, and Numbers tabs |
| `situation_report.html` | One-page report in English and Nepali |
| `facts.json` | All numbers used by the report and the copilot |
| `flood.geojson` | Flood mask polygons |

## View the dashboard

### Published dashboard

The latest hosted viewer is available here:

[Open the FloodWatch dashboard](https://shauryapriyam.github.io/Multimodal_AI_IITMANDI/outputs/index.html)

The published viewer contains the interactive Map, Report, and Numbers tabs.
Use the map controls below to zoom to places and toggle individual analysis
layers.

The dashboard is a static HTML output. Generate the viewer wrapper from the
`outputs` folder:

```powershell
python build_viewer.py --in outputs --out outputs/index.html
```

For reliable iframe and tile loading, serve the folder over HTTP instead of
opening the HTML file directly:

```powershell
python -m http.server 8000 --directory outputs
```

Open <http://localhost:8000/index.html>. If you generated another filename,
replace `index.html` in the URL, for example
<http://localhost:8000/index_3.html>.

### Map controls

- **Zoom:** use the `+` and `-` buttons in the upper-left corner, the mouse
  wheel, or trackpad pinch. Double-click zooms in. Drag the map to move to
  another place.
- **View a place:** zoom in until roads, settlements, and hospitals can be
  distinguished. Use the map labels and marker popups to identify a place.
  Zoom back out to compare the whole analysed bounding box.
- **Layer toggle:** use the layer control in the upper-right corner. Turn
  layers on or off independently to reduce visual overlap:
  - `Flood mask: Open water (new)` shows newly detected open-water polygons.
  - `Flood mask: Radar-change / debris-affected area` shows the second flood
    or debris-change mask.
  - `Buildings: intersect mask (red) / within 30 m (orange)` shows affected
    and nearby buildings.
  - `Roads (red) / bridges (purple) intersecting mask` shows affected
    transport links.
  - `Settlements (colour = hospital access)` shows access status by colour.
  - `Hospitals` shows hospital markers.
  - `Traced flood path (DEM)` shows the optional DEM-derived path.
- **Basemap:** the current generated dashboard intentionally keeps the
  **light CARTO basemap only**. It is the reliable fallback while the
  OpenStreetMap tile endpoint is blocked in some browser/network
  environments. Its attribution is shown in the lower-right corner.
- **Legend and summary:** the lower-left summary explains the event date,
  detected area, affected assets, and settlement-access colours. Expand or
  collapse the summary by clicking its heading.

### Inspect generated artifacts

The viewer separates the outputs so each can be checked independently:

1. Open `outputs/dashboard.html` to test only the interactive map.
2. Open `outputs/situation_report.html` to check the English and Nepali
   report.
3. Open `outputs/facts.json` to inspect the numeric source used by the report.
4. Open `outputs/flood.geojson` in a GeoJSON viewer or GIS application to
   inspect the detected flood polygons.
5. Open `outputs/index.html` to test the complete Map, Report, and Numbers
   tabbed viewer.

The `index.html` file embeds `dashboard.html` and
`situation_report.html` in iframes; it does not copy their map data. If the
map works when opening `dashboard.html` but not from `index.html`, check that
all files are in the same `outputs` directory and that the generated iframe
paths are correct.

### Check tile/network failures

If the map is blank or shows tile errors, open browser developer tools
(`F12`), select the **Console** and **Network** tabs, then reload the page.
In Network, filter for `tile`, `png`, or `cartocdn` and inspect the status:

- `200` means the tile loaded.
- `403` or `429` means the tile provider or a proxy rejected or rate-limited
  the request; do not interpret this as a missing flood layer.
- `404` usually means the tile URL or zoom coordinates are wrong.
- `blocked`, `CORS`, or `ERR_BLOCKED_BY_CLIENT` usually indicates a browser
  extension, privacy filter, firewall, or corporate proxy.

Also check the Console for JavaScript errors. A failed basemap request does
not remove the flood GeoJSON and marker layers, so toggle the basemap and
overlay layers separately to identify which request is failing. When testing
locally, use the HTTP server command above and try a private browser window
with extensions disabled. Do not commit API keys or paste `.env` contents
into the repository.

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

See the limitations in `FloodWatch_Report.docx`. The most important ones:

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
