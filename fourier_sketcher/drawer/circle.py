"""
Classes to represent circle plotting.
"""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


class Circle:
    """
    Logic for plotting Matplotlib circle.
    """

    def __init__(
        self, center: Tuple[float, float], radius: float, angle: float
    ) -> None:
        """
        Args:
            center: Center point of circle.
            radius: Radius of circle.
            angle: Radian angle to draw.
        """

        self._center = center
        self._radius = radius
        self._angle = angle

    @property
    def center(self) -> Tuple[float, float]:
        """ Pixel location of center. """

        return self._center

    @property
    def edge_point(self) -> Tuple[float, float]:
        """ Pixel location of point on radius. """

        x0, y0 = self.center  # pylint: disable=invalid-name
        return (
            x0 + self._radius * np.cos(self._angle),
            y0 + self._radius * np.sin(self._angle),
        )

    def draw(self) -> None:  # pylint: disable=invalid-name
        """
        Plot circle.

        Args:
            ax: Plot axis.
        """

        self._draw_center()
        self._draw_circle()
        self._draw_radius_at_angle()

    def _draw_center(self) -> None:
        """ Draw point at circle center. """

        plt.scatter(*self._center)

    def _draw_circle(self) -> None:
        """ Draw circle about center of radius. """

        # offset values to apply to center
        x_offset, y_offset = self.center

        # generate points on the unit circle
        points = [
            (np.cos(angle), np.sin(angle)) for angle in np.arange(0, 2 * np.pi, 0.01)
        ]

        # scale by radius
        points = [(self._radius * x, self._radius * y) for x, y in points]

        # offset to center point
        points = [(x + x_offset, y + y_offset) for x, y in points]

        xs, ys = zip(*points)  # pylint: disable=invalid-name
        plt.plot(xs, ys)

    def _draw_radius_at_angle(self) -> None:
        """ Draw line from center to circle at angle. """

        x0, y0 = self.center  # pylint: disable=invalid-name
        x1, y1 = self.edge_point  # pylint: disable=invalid-name

        plt.plot((x0, x1), (y0, y1))
