import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

import reg_bench.ode


dblpdl = reg_bench.ode.double_pendulum()

dy = dblpdl()
y0 = dblpdl.initial_conditions()
t = np.linspace(0, 10, 5 * 10 ** 3)

print(y0)

s = odeint(dy, y0, t)
for j in range(4):
    plt.figure(j)
    plt.plot(t, s[:, j])

plt.show()
