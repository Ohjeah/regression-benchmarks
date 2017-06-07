import functools


def harmonic_oscillator(omega=1.0):
    @functools.wraps(harmonic_oscillator)
    def dy(y, t):
        dy0 = y[1]
        dy1 = -omega**2 * y[0]
        return [dy0, dy1]
    return dy


def anharmonic_oscillator(omega=1.0, c=1.0, l=1.0):
    @functools.wraps(anharmonic_oscillator)
    def dy(y, t):
        dy0 = y[1]
        dy1 = - omega**2 * y[0] - l * y[0]**2 - c * y[1]
        return [dy0, dy1]
    return dy


def lorenz(s=10.0, r=28.0, b=8.0/3.0):
    @functools.wraps(lorenz)
    def dy(y, t):
        dy0 = s * (y[1] - y[0])
        dy1 = r * y[0] - y[1] - y[0] * y[2]
        dy2 = y[0] * y[1] - b * y[2]
        return [dy0, dy1, dy2]
    return dy


def van_der_pol(omega=1.0, a=0.1, b=0.01):
    @functools.wraps(van_der_pol)
    def dy(y, t):
        y0, y1 = y
        dy0 = y1
        dy1 = - omega**2 * y0 + a * y1 * (1 - b * y0**2)
        [dy0, dy1]
    return dy


def michaelis_menten(vmax=0.25, Km=0.1, rho=1.0):
    @functools.wraps(michaelis_menten)
    def dy(y, t):
        s, p = y
        dp = vmax * s**rho / (Km + s**rho)
        ds = -dp
        return [ds, dp]
    return dy
