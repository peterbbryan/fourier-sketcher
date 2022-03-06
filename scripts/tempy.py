# pylint: skip-file

import matplotlib.pyplot as plt
import numpy as np

from fourier_sketcher.drawer import Circle
from fourier_sketcher.oscillator import Oscillator

fig = plt.figure()
ax = plt.gca()
max_n = 10

plt.ion()

xs = []
ys = []

for t in np.arange(0, 100, 0.01):

    edge = (0.0, 0.0)

    for i in range(max_n):
        oscillator = Oscillator(frequency=i)
        circle = Circle(center=edge, radius=1 / (i + 1), angle=oscillator.angle(t))
        circle.draw(ax)
        edge = circle.edge_point
        if i == max_n - 1:
            x, y = edge
            xs.append(x)
            ys.append(y)
            plt.scatter(xs, ys, linewidth=1)

    plt.axis("square")
    plt.axis("off")

    plt.draw()
    plt.pause(0.000000001)
    plt.clf()
