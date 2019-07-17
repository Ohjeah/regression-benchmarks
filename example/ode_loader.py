"""
ODE loader
==========
"""
import matplotlib.pyplot as plt
import numpy as np

from reg_bench.ode import all_loaders


shear_flow = all_loaders["shear_flow"]()

plt.plot(shear_flow.t, shear_flow.data)
plt.show()
