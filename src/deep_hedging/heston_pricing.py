from __future__ import annotations

import numpy as np
from scipy.integrate import quad


def _cf(u, tau, s, v, r, kappa, theta, xi, rho):
    iu = 1j * u
    if xi < 1e-10:
        var = theta * tau + (v - theta) * (1 - np.exp(-kappa * tau)) / max(kappa, 1e-12)
        return np.exp(iu * (np.log(s) + r * tau - 0.5 * var) - 0.5 * u * u * var)
    a = kappa * theta
    b = kappa - rho * xi * iu
    d = np.sqrt(b * b + xi * xi * (u * u + iu))
    g = (b - d) / (b + d)
    ed = np.exp(-d * tau)
    C = iu * r * tau + (a / (xi * xi)) * ((b - d) * tau - 2 * np.log((1 - g * ed) / (1 - g)))
    D = ((b - d) / (xi * xi)) * ((1 - ed) / (1 - g * ed))
    return np.exp(C + D * v + iu * np.log(s))


def heston_call_price(s, strike, tau, *, v, kappa, theta, xi, rho, rate=0.0, integration_limit=150.0):
    if tau <= 0:
        return max(s - strike, 0.0)
    phi_mi = _cf(-1j, tau, s, v, rate, kappa, theta, xi, rho)
    logk = np.log(strike)

    def p1int(u):
        return np.real(
            np.exp(-1j * u * logk) * _cf(u - 1j, tau, s, v, rate, kappa, theta, xi, rho) / (1j * u * phi_mi)
        )

    def p2int(u):
        return np.real(np.exp(-1j * u * logk) * _cf(u, tau, s, v, rate, kappa, theta, xi, rho) / (1j * u))

    p1 = 0.5 + quad(p1int, 1e-8, integration_limit, limit=300, epsabs=1e-8, epsrel=1e-7)[0] / np.pi
    p2 = 0.5 + quad(p2int, 1e-8, integration_limit, limit=300, epsabs=1e-8, epsrel=1e-7)[0] / np.pi
    return float(s * p1 - strike * np.exp(-rate * tau) * p2)


def heston_delta_fd(s, strike, tau, *, relative_step=1e-4, **params):
    h = max(relative_step * s, 1e-4)
    up = heston_call_price(s + h, strike, tau, **params)
    dn = heston_call_price(max(s - h, 1e-8), strike, tau, **params)
    return (up - dn) / (2 * h)
