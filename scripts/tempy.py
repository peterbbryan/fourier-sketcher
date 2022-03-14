# pylint: skip-file

import matplotlib.pyplot as plt
import numpy as np

from fourier_sketcher.drawer import Circle
from fourier_sketcher.edger import Edger
from fourier_sketcher.oscillator import Oscillator
from fourier_sketcher.sketcher import Sketcher

edger = Edger("./resources/sample.jpeg")

sketcher = Sketcher(edger)
sketcher.make_gif("temp.gif")
