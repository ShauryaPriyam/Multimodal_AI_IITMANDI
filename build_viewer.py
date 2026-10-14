"""Build one FloodWatch page from the files in an outputs folder.

Usage:
    python build_viewer.py
    python build_viewer.py --in outputs --out outputs/index.html
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path

NUM_TOKEN = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

FOOTER = (
    "Contains modified Copernicus Sentinel data 2026.",
    "Produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.",
    "© OpenStreetMap contributors.",
    "Educational prototype, not an operational tool. Not field-verified.",
)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #fff;
    color: #172033;
    font-family: "Noto Sans", "Noto Sans Devanagari", sans-serif;
    font-size: 16px;
    line-height: 1.5;
  }
  header { background: #0a2540; color: #fff; padding: 0.9rem 1.1rem; }
  header h1 { margin: 0; font-size: 1.35rem; font-weight: 650; letter-spacing: -0.02em; }
  header p { margin: 0.2rem 0 0; font-size: 0.95rem; }
  .tabs {
    display: flex;
    gap: 0.35rem;
    padding: 0.65rem 1rem 0;
    background: #f3f6fa;
    border-bottom: 1px solid #d5dbe6;
    overflow-x: auto;
  }
  .tabs button {
    font: inherit;
    font-size: 0.95rem;
    padding: 0.55rem 0.95rem;
    border: 1px solid transparent;
    border-bottom: 0;
    background: transparent;
    color: #0a2540;
    cursor: pointer;
    border-radius: 0.35rem 0.35rem 0 0;
    white-space: nowrap;
  }
  .tabs button[aria-selected="true"] {
    background: #fff;
    border-color: #d5dbe6;
    margin-bottom: -1px;
    border-bottom: 1px solid #fff;
    font-weight: 650;
  }
  main { flex: 1 0 auto; display: flex; flex-direction: column; }
  .panel { flex: 1 0 auto; }
  .panel[hidden] { display: none; }
  .frame-panel { display: flex; flex-direction: column; min-height: 70vh; }
  .frame-panel iframe { flex: 1 1 auto; width: 100%; min-height: 70vh; border: 0; background: #fff; }
  .report-bar { padding: 0.65rem 1rem; border-bottom: 1px solid #d5dbe6; }
  .report-bar button {
    font: inherit;
    background: #0a2540;
    color: #fff;
    border: 0;
    padding: 0.5rem 0.85rem;
    cursor: pointer;
  }
  .missing { margin: 1rem; padding: 1rem 1.1rem; background: #f6f8fb; border: 1px solid #d5dbe6; }
  #panel-numbers { padding: 1rem 1.1rem 1.5rem; }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 0.75rem; }
  .card { border: 1px solid #e1e6ee; padding: 0.75rem 0.85rem; background: #fff; }
  .card.wide { grid-column: 1 / -1; }
  .k { color: #5c6b7a; font-size: 0.8rem; }
  .v { margin-top: 0.2rem; font-size: 1.45rem; font-weight: 650; overflow-wrap: anywhere; }
  .card.wide .v { font-size: 1rem; font-weight: 400; }
  h2 { margin: 1.35rem 0 0.45rem; font-size: 1.05rem; }
  h3 { margin: 1rem 0 0.35rem; font-size: 0.95rem; }
  .table-wrap { overflow-x: auto; max-width: 100%; }
  table { width: 100%; border-collapse: collapse; }
  table.data { width: max-content; min-width: 100%; }
  th, td { text-align: left; vertical-align: top; padding: 0.4rem 0.5rem; border-bottom: 1px solid #e1e6ee; }
  th { color: #5c6b7a; font-weight: 650; }
  ul { margin: 0.2rem 0 0.4rem; padding-left: 1.2rem; }
  footer { padding: 1rem 1.1rem 1.4rem; border-top: 1px solid #d5dbe6; color: #1c2430; font-size: 0.82rem; line-height: 1.45; }
  footer p { margin: 0.28rem 0; overflow-wrap: anywhere; }
  @media (max-width: 640px) {
    header h1 { font-size: 1.2rem; }
    .tabs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); padding-left: 0.35rem; padding-right: 0.35rem; }
    .tabs button { width: 100%; min-width: 0; padding: 0.6rem 0.15rem; text-align: center; }
    .v { font-size: 1.25rem; }
    table.kv, table.kv tr, table.kv th, table.kv td { display: block; width: 100%; }
    table.kv th { border: 0; padding-bottom: 0; }
    table.kv td { padding-top: 0.1rem; }
  }
</style>
</head>
<body>
<header>
<h1>FloodWatch</h1>
@@EVENT@@
</header>
<div class="tabs" role="tablist">
<button type="button" role="tab" id="tab-map" data-tab="map" aria-selected="true" aria-controls="panel-map">Map</button>
<button type="button" role="tab" id="tab-report" data-tab="report" aria-selected="false" aria-controls="panel-report">Report</button>
<button type="button" role="tab" id="tab-numbers" data-tab="numbers" aria-selected="false" aria-controls="panel-numbers">Numbers</button>
</div>
<main>
<section class="panel frame-panel" role="tabpanel" id="panel-map" data-panel="map" aria-labelledby="tab-map">
@@MAP@@
</section>
<section class="panel frame-panel" role="tabpanel" id="panel-report" data-panel="report" aria-labelledby="tab-report" hidden>
@@REPORT@@
</section>
<section class="panel" role="tabpanel" id="panel-numbers" data-panel="numbers" aria-labelledby="tab-numbers" hidden>
@@NUMBERS@@
</section>
</main>
<footer>
@@FOOTER@@
</footer>
<script>
(function () {
  function isScalar(value) {
    return value === null || typeof value === "string" || typeof value === "number" || typeof value === "boolean";
  }

  function formatScalar(value, key) {
    if (value === null) return "null";
    if (typeof value === "string") {
      if (value.trim() === "") return "(unnamed)";
      return value;
    }
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "number") return JSON.stringify(value);
    return String(value);
  }

  function renderList(items, key) {
    var allObjects = items.length > 0 && items.every(function (item) {
      return item !== null && typeof item === "object" && !Array.isArray(item);
    });
    if (allObjects) return renderObjectTable(items);
    var ul = document.createElement("ul");
    items.forEach(function (item) {
      var li = document.createElement("li");
      if (isScalar(item)) li.textContent = formatScalar(item, key);
      else if (Array.isArray(item)) li.appendChild(renderList(item, key));
      else renderObject(item, li);
      ul.appendChild(li);
    });
    return ul;
  }

  function renderObjectTable(rows) {
    var columns = [];
    rows.forEach(function (row) {
      Object.keys(row).forEach(function (key) {
        if (columns.indexOf(key) === -1) columns.push(key);
      });
    });
    var wrap = document.createElement("div");
    wrap.className = "table-wrap";
    var table = document.createElement("table");
    table.className = "data";
    var head = document.createElement("tr");
    columns.forEach(function (key) {
      var th = document.createElement("th");
      th.textContent = key;
      head.appendChild(th);
    });
    var thead = document.createElement("thead");
    thead.appendChild(head);
    table.appendChild(thead);
    var body = document.createElement("tbody");
    rows.forEach(function (row) {
      var tr = document.createElement("tr");
      columns.forEach(function (key) {
        var td = document.createElement("td");
        putValue(td, row[key], key);
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
    wrap.appendChild(table);
    return wrap;
  }

  function putValue(parent, value, key) {
    if (isScalar(value)) {
      parent.textContent = formatScalar(value, key);
      return;
    }
    if (Array.isArray(value)) {
      parent.appendChild(renderList(value, key));
      return;
    }
    if (value && typeof value === "object") renderObject(value, parent);
  }

  function renderObject(obj, parent) {
    var scalars = [];
    var rest = [];
    Object.keys(obj).forEach(function (key) {
      (isScalar(obj[key]) ? scalars : rest).push(key);
    });
    if (scalars.length) {
      var wrap = document.createElement("div");
      wrap.className = "table-wrap";
      var table = document.createElement("table");
      table.className = "kv";
      scalars.forEach(function (key) {
        var tr = document.createElement("tr");
        var th = document.createElement("th");
        th.textContent = key;
        var td = document.createElement("td");
        td.textContent = formatScalar(obj[key], key);
        tr.appendChild(th);
        tr.appendChild(td);
        table.appendChild(tr);
      });
      wrap.appendChild(table);
      parent.appendChild(wrap);
    }
    rest.forEach(function (key) {
      parent.appendChild(renderSection(key, obj[key], 1));
    });
  }

  function renderSection(key, value, level) {
    var section = document.createElement("section");
    var heading = document.createElement(level === 0 ? "h2" : "h3");
    heading.textContent = key;
    section.appendChild(heading);
    putValue(section, value, key);
    return section;
  }

  function renderCard(key, value) {
    var card = document.createElement("article");
    card.className = "card";
    if (typeof value === "string" && value.length > 80) card.className = "card wide";
    var label = document.createElement("div");
    label.className = "k";
    label.textContent = key;
    var shown = document.createElement("div");
    shown.className = "v";
    shown.textContent = formatScalar(value, key);
    card.appendChild(label);
    card.appendChild(shown);
    return card;
  }

  function renderRoot(data, parent) {
    if (isScalar(data)) {
      parent.textContent = formatScalar(data, "");
      return;
    }
    if (Array.isArray(data)) {
      parent.appendChild(renderList(data, ""));
      return;
    }
    var scalars = [];
    var rest = [];
    Object.keys(data).forEach(function (key) {
      (isScalar(data[key]) ? scalars : rest).push(key);
    });
    if (scalars.length) {
      var cards = document.createElement("div");
      cards.className = "cards";
      scalars.forEach(function (key) {
        cards.appendChild(renderCard(key, data[key]));
      });
      parent.appendChild(cards);
    }
    rest.forEach(function (key) {
      parent.appendChild(renderSection(key, data[key], 0));
    });
  }

  var tabs = document.querySelectorAll("[data-tab]");
  var panels = document.querySelectorAll("[data-panel]");
  function show(id) {
    tabs.forEach(function (tab) {
      var on = tab.getAttribute("data-tab") === id;
      tab.setAttribute("aria-selected", on ? "true" : "false");
    });
    panels.forEach(function (panel) {
      if (panel.getAttribute("data-panel") === id) panel.removeAttribute("hidden");
      else panel.setAttribute("hidden", "");
    });
  }
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { show(tab.getAttribute("data-tab")); });
  });

  var printButton = document.getElementById("print-report");
  if (printButton) {
    printButton.addEventListener("click", function () {
      var frame = document.getElementById("report-frame");
      if (!frame || !frame.contentWindow) return;
      frame.contentWindow.focus();
      frame.contentWindow.print();
    });
  }

  var dataEl = document.getElementById("facts-data");
  var mount = document.getElementById("numbers-root");
  if (!dataEl || !mount) return;
  try {
    renderRoot(JSON.parse(dataEl.textContent), mount);
  } catch (err) {
    mount.textContent = "facts.json could not be read.";
  }
})();
</script>
</body>
</html>
"""


CARTO_TILE_URL = re.compile(
    r"https://(?:\{s\}\.)?basemaps\.cartocdn\.com/[A-Za-z0-9_./{}@+-]+(?:\?[^\"'\\]*)?"
)


def env_values() -> dict[str, str]:
    path = Path(__file__).resolve().parent / ".env"
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        values[name.strip()] = value.strip().strip('"').strip("'")
    return values


def carto_basemap_key() -> str:
    values = env_values()
    for name in ("CARTO_BASEMAP_KEY", "CARTO_API_KEY"):
        value = os.environ.get(name, "").strip() or values.get(name, "").strip()
        if value:
            return value
    return ""


def apply_carto_key(dashboard: Path) -> str:
    """Put the basemap key on the Carto tile URL. The key stays in .env."""
    key = carto_basemap_key()
    if not key:
        return "CARTO basemap key: not set"
    if re.fullmatch(r"[A-Za-z0-9._~-]+", key) is None:
        return "CARTO basemap key: not applied (unsupported characters)"
    text = dashboard.read_text(encoding="utf-8")
    url = (
        "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/"
        "{z}/{x}/{y}{r}.png?key=" + key
    )
    updated, count = CARTO_TILE_URL.subn(url, text)
    if count == 0:
        return "CARTO basemap key: dashboard has no Carto tile URL"
    if updated != text:
        dashboard.write_text(updated, encoding="utf-8", newline="\n")
    return "CARTO basemap key: applied"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the FloodWatch viewer page from an outputs folder.")
    parser.add_argument("--in", dest="src", default="outputs", help="Folder that holds the pipeline outputs")
    parser.add_argument("--out", default="outputs/index.html", help="HTML file to write")
    return parser.parse_args(argv)


def load_facts(path: Path):
    if not path.is_file():
        return None, None
    try:
        raw = path.read_text(encoding="utf-8-sig")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return None, False
    return data, raw


def event_line(data) -> str:
    if not isinstance(data, dict) or "event_date" not in data:
        return ""
    value = data["event_date"]
    if isinstance(value, (dict, list)) or value is None:
        return ""
    return f"<p>{html.escape(str(value))}</p>"


def missing(name: str) -> str:
    return f'<p class="missing">{html.escape(name)} was not found.</p>'


def frame(title: str, src: str, element_id: str = "") -> str:
    ident = f' id="{element_id}"' if element_id else ""
    return f'<iframe{ident} title="{html.escape(title)}" src="{html.escape(src)}"></iframe>'


def relative_href(out_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target, start=out_file.parent)).as_posix()


def number_tokens(raw: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    in_str = False
    escaped = False
    while i < len(raw):
        char = raw[i]
        if in_str:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_str = False
            i += 1
            continue
        if char == '"':
            in_str = True
            i += 1
            continue
        if char == ":":
            j = i + 1
            while j < len(raw) and raw[j] in " \t\r\n":
                j += 1
            match = NUM_TOKEN.match(raw, j)
            if match:
                tokens.append(match.group(0))
                i = match.end()
                continue
        i += 1
    return tokens


def stamp(value, tokens: list[str], pos: int):
    """Replace JSON numbers with the exact text stored in the file."""
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            out[key], pos = stamp(item, tokens, pos)
        return out, pos
    if isinstance(value, list):
        out = []
        for item in value:
            item, pos = stamp(item, tokens, pos)
            out.append(item)
        return out, pos
    if isinstance(value, bool):
        return value, pos
    if isinstance(value, (int, float)):
        if pos >= len(tokens):
            raise ValueError("number tokens do not match the file")
        return tokens[pos], pos + 1
    return value, pos


def embed_json(raw: str) -> str:
    try:
        stamped, pos = stamp(json.loads(raw), number_tokens(raw), 0)
        if pos != len(number_tokens(raw)):
            raise ValueError("number tokens do not match the file")
        text = json.dumps(stamped, ensure_ascii=False)
    except (json.JSONDecodeError, ValueError, TypeError):
        text = raw
    return text.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build(src: Path, out_file: Path) -> None:
    facts_path = src / "facts.json"
    dashboard_path = src / "dashboard.html"
    report_path = src / "situation_report.html"
    data, raw = load_facts(facts_path)

    print(f"Input folder: {src}")
    if facts_path.is_file() and raw is False:
        print("facts.json: found, but it is not valid JSON")
    else:
        print(f"facts.json: {'found' if facts_path.is_file() else 'not found'}")
    if dashboard_path.is_file():
        print("dashboard.html: found")
        print(apply_carto_key(dashboard_path))
    else:
        print("dashboard.html: not found")
    print(f"situation_report.html: {'found' if report_path.is_file() else 'not found'}")

    if dashboard_path.is_file():
        map_html = frame("Map", relative_href(out_file, dashboard_path))
    else:
        map_html = missing("dashboard.html")

    if report_path.is_file():
        report_html = (
            '<div class="report-bar"><button type="button" id="print-report">Print / Save as PDF</button></div>'
            + frame("Report", relative_href(out_file, report_path), "report-frame")
        )
    else:
        report_html = missing("situation_report.html")

    if isinstance(raw, str):
        numbers_html = (
            f'<script type="application/json" id="facts-data">{embed_json(raw)}</script>'
            '<div id="numbers-root"></div>'
        )
    elif raw is False:
        numbers_html = '<p class="missing">facts.json could not be read.</p>'
    else:
        numbers_html = missing("facts.json")

    title = "FloodWatch"
    if isinstance(data, dict) and isinstance(data.get("event_date"), (str, int, float)) and not isinstance(data.get("event_date"), bool):
        title = f"FloodWatch — {data['event_date']}"

    footer_html = "".join(f"<p>{html.escape(line)}</p>" for line in FOOTER)
    page = (
        PAGE.replace("@@TITLE@@", html.escape(title))
        .replace("@@EVENT@@", event_line(data))
        .replace("@@MAP@@", map_html)
        .replace("@@REPORT@@", report_html)
        .replace("@@NUMBERS@@", numbers_html)
        .replace("@@FOOTER@@", footer_html)
    )
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out_file}")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    build(Path(args.src), Path(args.out))


if __name__ == "__main__":
    main()
