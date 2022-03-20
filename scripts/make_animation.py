# pylint: skip-file

import pathlib
from tkinter import N
from typing import Any, Dict, Optional

import fire

from fourier_sketcher.edger import Edger
from fourier_sketcher.sketcher import Sketcher


def animate(
    input_image_path_str: str,
    output_image_path_str: str,
    edger_kwargs: Optional[Dict[str, Any]] = None,
    sketcher_kwargs: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Animate gif of outline sketch using Fourier transform.

    Args:
        input_image_path_str: Path to input image
        output_image_path_str: Output path to gif.
        edger_kwargs: Keyword arguments to determine Canny edge detection params.
        sketcher_kwargs: Keyword arguments to determine sketching params.
    """

    if edger_kwargs is None:
        edger_kwargs = {}

    if sketcher_kwargs is None:
        sketcher_kwargs = {}

    suffix = pathlib.Path(output_image_path_str).suffix
    assert suffix == ".gif", "Only .gif outputs are supported."

    edger = Edger(input_image_path_str, **edger_kwargs)

    sketcher = Sketcher(edger, **sketcher_kwargs)
    sketcher.make_gif(output_image_path_str)


if __name__ == "__main__":
    fire.Fire(animate)
