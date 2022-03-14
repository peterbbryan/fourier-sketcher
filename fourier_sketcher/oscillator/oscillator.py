"""
Classes to represent arbitrary oscillators.
"""

import numpy as np


class Oscillator:  # pylint: disable=too-few-public-methods
    """
    Logic for a simple oscillator.
    """

    def __init__(self, frequency: float, phase: float = 0) -> None:
        """
        Args:
            frequency: Frequency of oscillator.
            phase: Phase offset of oscillator.
        """

        self._frequency = frequency
        self._phase = phase

    def angle(self, t: float) -> float:  # pylint: disable=invalid-name
        """
        Angle value for arbitrary time t.e

        Args:
            t: Time.
        Returns:
            Angle at time.
        """

        x = np.cos(self._frequency * t + self._phase)  # pylint: disable=invalid-name
        y = np.sin(self._frequency * t + self._phase)  # pylint: disable=invalid-name

        return np.arctan2(y, x)
