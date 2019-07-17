"""
Michaelis Menten Kinetics
=========================
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

import reg_bench.ode


t = np.linspace(0, 10, 5 * 10 ** 2)
x0 = [1, 0]


noise = 0.01

x, dx = reg_bench.ode.generate_ode_data(
    reg_bench.ode.michaelis_menten, x0, t, noise_amplitude=noise, ode_params=dict(rho=1.3)
)

plt.plot(t, x)
plt.show()
