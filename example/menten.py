import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import benchmark.ode


dy = benchmark.ode.michaelis_menten(rho=1.3)
t = np.linspace(0, 10, 5*10**5)
x0 = [1, 0]
s = odeint(dy, x0, t)
plt.plot(t, s)

plt.show()
