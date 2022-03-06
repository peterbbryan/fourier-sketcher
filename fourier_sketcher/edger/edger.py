"""
Classes to represent image loading.
"""

import pathlib


class Edger:  # pylint: disable=too-few-public-methods
    """
    Logic for loading image from file.
    """

    def __init__(self, path: str) -> None:
        """
        Args:
            path: Path to file to load.
        """

        self._path = path

        extension = pathlib.Path(path)

        del extension

    @staticmethod
    def _from_jpeg(path: pathlib.Path):
        """ Load image at path. """

        del path
