"""Flood segmentation model.

Train and evaluate only on Kuro Siwo or Sen1Floods11. Copernicus EMS,
UNOSAT, and post-event maps are not training labels. The checkpoint file
is ``weights/flood_model.pt``.
"""

from __future__ import annotations

from pathlib import Path


class FloodModel:
    """Pixel model that marks flood water in a raster tile.

    The planned input stack is pre/post Sentinel-1 backscatter, optional
    Sentinel-2 indices, and slope derived from Copernicus DEM. The stack
    depth is ``in_channels``.
    """

    def __init__(self, in_channels: int = 8) -> None:
        """Create an untrained network.

        Parameters
        ----------
        in_channels:
            Number of bands in each input tile. The default matches the
            planned Sentinel-1, Sentinel-2, and DEM stack.
        """
        raise NotImplementedError

    def predict_tile(self, tile: object) -> object:
        """Score one tile.

        Parameters
        ----------
        tile:
            Array shaped ``(channels, height, width)`` with ``channels``
            equal to ``in_channels``.

        Returns
        -------
        object
            Flood probability array shaped ``(height, width)``, values
            between 0 and 1.
        """
        raise NotImplementedError


def load_weights(weights: Path, in_channels: int = 8) -> FloodModel:
    """Load ``weights/flood_model.pt``.

    Parameters
    ----------
    weights:
        Checkpoint written for ``FloodModel``.
    in_channels:
        Channel count stored for that checkpoint. It must match the tensor
        ``pipeline.infer`` builds.

    Returns
    -------
    FloodModel
        Model with the checkpoint loaded, ready for ``predict_tile``.

    Raises
    ------
    PipelineError
        If ``weights`` is missing or the checkpoint does not match
        ``in_channels``.
    """
    raise NotImplementedError
