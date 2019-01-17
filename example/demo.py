import matplotlib.pyplot as plt
import numpy as np

from reg_bench.ode.differentiate import diff
from reg_bench.ode.integrate import add_measurement_noise


x = np.linspace(0, 2 * np.pi, 50)
y = add_measurement_noise(np.sin(x), noise_amplitude=0.1)
dy = diff(x, y, order=1, n_points=5, kind="finitediff")
dy_old = diff(x, y.reshape(-1, 1), kind="simple_finite_diff")
chartrand = diff(x, y, kind="tvregdiff", scale="small")

# plt.plot(x, y, "o--", label="f")
plt.plot(x, dy[:, 0], "x--", label="f'_finitediff")
plt.plot(x, dy_old, "x--", label="f'_old")
plt.plot(x, chartrand, label="f'_chartrand")
plt.plot(x, np.cos(x), label="f'_analytic")
plt.ylim((-5, 5))
plt.xlabel("x")
plt.legend()
plt.show()
