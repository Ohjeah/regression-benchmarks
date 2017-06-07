import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import benchmark.ode


yeast = benchmark.ode.yeast_glycolysis()

dy = yeast()


for i in range(3):
    y0 = yeast.initial_conditions(noise=True)
    t = np.linspace(0, 5, 5*10**5)

    s = odeint(dy, y0, t)
    for j in range(3):
        plt.figure(j)
        plt.plot(t, s[:, j])

plt.show()
