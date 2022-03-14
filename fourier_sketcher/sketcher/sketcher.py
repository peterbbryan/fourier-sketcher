"""
Classes to extract oscillators for an outline.
"""

import io
from functools import lru_cache
from typing import List, Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm
from PIL import Image

from fourier_sketcher.drawer import Circle
from fourier_sketcher.edger import Edger
from fourier_sketcher.oscillator import Oscillator


class Sketcher:  # pylint: disable=too-few-public-methods
    """
    Logic for sketching an outline using Fourier based oscillators.
    """

    def __init__(
        self, edger: Edger, n_oscillators: int = 128, n_steps: int = 200
    ) -> None:
        """
        Args:
            edger: Representation of image edges.
            n_oscillators: Number of oscillators.
            n_steps: Number of steps to sample.
        """

        self._fig = plt.figure()
        self._edger = edger
        self._n_oscillators = n_oscillators
        self._n_steps = n_steps

    def make_gif(self, path_str: str) -> None:
        """
        Make gif of outline.

        Args:
            path_str: Path to write gif to.
        """

        plt.ion()

        fft_values, fft_bins = self._get_frequency_components()
        plots, points = [], []

        for step in tqdm.tqdm(np.linspace(0, 2 * np.pi, self._n_steps)):

            edge = (0.0, 0.0)

            for i in range(self._n_oscillators):

                mag = np.abs(fft_values[i])
                ang = np.angle(fft_values[i])

                oscillator = self._get_oscillator(frequency=fft_bins[i], phase=ang)
                circle = self._get_circle(
                    center=edge, radius=mag, angle=oscillator.angle(step)
                )
                circle.draw()
                edge = circle.edge_point

                if i == self._n_oscillators - 1:
                    points.append(edge)

            self._make_plot(points)

            plot_img_np = self._get_arr_from_fig()
            plots.append(Image.fromarray(plot_img_np))

            plt.clf()

        self._write_gif(plots, path_str)

    def _get_arr_from_fig(self, dpi: int = 90) -> np.ndarray:
        """
        Get np.ndarray from a figure.

        Args:
            fig: Matplotlib Figure.
            dpi: Resolution.
        Returns:
            Numpy array of image contents.
        """

        buf = io.BytesIO()
        self._fig.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        buf.close()
        img = cv2.imdecode(img_arr, 1)  # pylint: disable=no-member
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member

        return img

    def _get_frequency_components(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get frequency components from outline.

        Returns:
            Tuple of frequency values and bin centers.
        """

        complex_sequence = self._sort_points(self._edger.complex_sequence)

        fft_values = np.fft.fft(complex_sequence)
        fft_bins = np.fft.fftfreq(len(fft_values), d=1 / (len(fft_values)))

        # make this less stupid
        fft_values = fft_values[np.abs(fft_bins) <= (self._n_oscillators / 2)]
        fft_bins = fft_bins[np.abs(fft_bins) <= (self._n_oscillators / 2)]

        fft_bins = fft_bins[np.argsort(-np.abs(fft_values))]
        fft_values = fft_values[np.argsort(-np.abs(fft_values))]

        return fft_values, fft_bins

    @staticmethod
    def _make_plot(points: List[Tuple[float, float]]) -> None:
        """
        Plot outline so far.

        Args:
            points: x, y points to plot.
        """

        plt.scatter(*list(zip(*points)), linewidth=1)

        plt.draw()
        plt.axis("square")
        plt.axis("off")

    @staticmethod
    def _sort_points(
        complex_sequence: np.ndarray, stopping_threshold: float = 10
    ) -> np.ndarray:
        """
        Arrange points so that neighbors are near each other in sequence.

        Args:
            complex_sequence: Points as complex array.
        Returns:
            Sorted points to minimize sequential differences.
        """

        reordered: List[np.complex128] = []
        current_point = complex_sequence[0]
        complex_sequence[0] = np.inf

        while len(reordered) < complex_sequence.shape[0]:

            if np.min(np.abs(complex_sequence - current_point)) > stopping_threshold:
                break

            min_dist_ind = np.argmin(np.abs(complex_sequence - current_point))
            reordered.append(current_point)
            current_point = complex_sequence[min_dist_ind]
            complex_sequence[min_dist_ind] = np.inf

        return np.array(reordered)

    @staticmethod
    def _write_gif(
        plots: List[Image.Image],
        path_str: str,
        last_frame_repeats: int = 100,
        duration: int = 60,
    ) -> None:
        """
        Write animated gif.

        Args:
            plots: Output plots to write.
            path_str: Path to output gif.
            last_frame_repeats: Number of repeats of last still.
            duration: Duration in seconds.
        """

        for _ in range(last_frame_repeats):
            plots.append(plots[-1])

        plots[0].save(
            path_str, save_all=True, append_images=plots[1:], duration=duration, loop=0,
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_circle(*args, **kwargs) -> Circle:
        """ Get cached circle. """

        return Circle(*args, **kwargs)

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_oscillator(*args, **kwargs) -> Oscillator:
        """ Get cached oscillator. """

        return Oscillator(*args, **kwargs)
