"""
Classes to represent image loading.
"""

import pathlib

import cv2 as cv
import numpy as np
from PIL import Image


class Edger:  # pylint: disable=too-few-public-methods
    """
    Logic for loading image from file.
    """

    def __init__(self, path_str: str) -> None:
        """
        Args:
            path: Path to file to load.
        """

        extension = pathlib.Path(path_str).suffix

        extension_map = {".jpeg": self._from_jpeg, ".jpg": self._from_jpeg}.get(
            extension
        )

        assert extension_map is not None, "No mapping for extension"

        self._image = extension_map(path_str)

    @property
    def binary_mask(self):
        """ Binary mask from image. """

        im = np.array(self._image)  # pylint: disable=invalid-name
        edges = cv.Canny(im, 100, 150)  # pylint:disable=no-member

        return np.array(edges).astype(np.bool)

    @property
    def complex_sequence(self) -> np.ndarray:
        """ Binary pixel coordinates as complex sequence. """

        # row/col to x/y will impart a directional flip on coordinates
        locs = np.argwhere(np.flipud(self.binary_mask)).astype(np.complex128)
        n_rows, n_cols = self.binary_mask.shape

        # center about the origin
        rows = locs[:, 0] - (n_rows // 2)
        columns = locs[:, 1] - (n_cols // 2)

        # represent y values with i
        rows *= 1j

        # restructure to x, y order
        return rows + columns

    @staticmethod
    def _from_jpeg(path_str: str) -> Image:
        """ Load image at path. """

        return Image.open(path_str)
