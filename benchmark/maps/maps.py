import functools

import numpy as np


def henon(a=1.4, b=0.3):
    @functools.wraps(henon)
    def f(state):
        x, y = state
        return y + 1 - a * x**2, b * x
    return f


def chirikov(K=1):
    @functools.wraps(chirikov)
    def f(state):
        p, theta = state
        p_1 = p + K*np.sin(theta)
        theta_1 = theta + p_1
        return p_1, theta_1
    return f


def logistic(r=3.18):
    @functools.wraps(logistic)
    def f(x):
        return r*x*(1 - x)
    return f


def bogdanov(eps, k , mu):
    @functools.wraps(bogdanov)
    def f(state):
        x, y = state
        return x + y, (1 + eps)*y + k*x*(x - 1) + mu*x*y


def duffing(a=2.75, b=0.15):
    @functools.wraps(duffing)
    def f(state):
        x, y = state
        return y, -b*x + a*y -y**3
    return f


def tinkerbell(a=0.9, b=-0.6013, c=2.0, d=0.5):
    @functools.wraps(tinkerbell)
    def f(state):
        x, y = state
        return x**2 - y**2 + a*x + b*y, 2*x*y + c*x + d*y
    return f