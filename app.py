"""Streamlit dashboard for flood extent, damage, and road cut-off.

Running an analysis is not implemented. ``main`` is the entry point that
will collect a bounding box and a flood date and call the pipeline.
"""

from __future__ import annotations


def main() -> None:
    """Open the dashboard.

    Inputs are a WGS84 bounding box and a flood date. No place is built in.
    The page will show three results:

    1. Where the flood hit, from the Sentinel-1 pair and the flood model.
    2. What was damaged, from pre-event buildings, roads, and bridges.
    3. Who is cut off, from the pre-event road graph.

    Every view ends with a footer that prints
    ``pipeline.utils.ATTRIBUTIONS`` one line at a time, unchanged.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
