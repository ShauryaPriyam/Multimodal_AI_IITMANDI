"""Run the flood segmentation model and write a mask GeoTIFF.

The checkpoint is ``weights/flood_model.pt``, trained on Kuro Siwo or
Sen1Floods11. Copernicus EMS and UNOSAT maps are not model inputs.
"""

from __future__ import annotations

from pathlib import Path


def predict_flood_mask(
    rasters: dict[str, Path],
    weights: Path,
    output_path: Path,
) -> Path:
    """Tile the downloaded rasters, run the flood model, and write a mask.

    Parameters
    ----------
    rasters:
        Paths returned by ``pipeline.satellite.download_rasters``.
        ``vv_pre``, ``vv_post``, and ``dem`` are required. VH and Sentinel-2
        paths are used when they are present.
    weights:
        Checkpoint path. The project default is ``weights/flood_model.pt``.
    output_path:
        Destination GeoTIFF. Parent directories may be created on write.

    Returns
    -------
    Path
        ``output_path``. Pixel value 1 is flood, 0 is not flood, and 255
        is nodata. The grid is a projected metre grid covering the same
        bounding box as ``rasters``, not a grid fixed to one study area.

    Raises
    ------
    PipelineError
        If ``weights`` is missing, the checkpoint does not match the model,
        or a required raster is absent.
    """
    raise NotImplementedError
