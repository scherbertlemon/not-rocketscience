import numpy as np


canonical_weird_parameterset = (4, 6, 0.2, 4, 1.2)
canonical_newton_parameterset = (0.25, 0.01)


def exp2(b2, s2):
    def f(r):
        return np.exp(-b2 * (r - s2))
    return f


def ln(b1, s1):
    def f(r):
        return np.log(b1 * (r + s1))
    return f


def weird_gravity_potential(A, b1, s1, b2, s2):
    def f(r):
        return A * ln(b1, s1)(r) * exp2(b2, s2)(r)
    return f


def weird_gravity_force(A, b1, s1, b2, s2):
    def f(r):
        return A * exp2(b2, s2)(r) * (1/(r + s1) - b2 * ln(b1, s1)(r))
    return f


def weird_gravity_force_derivative(A, b1, s1, b2, s2):
    def f(r):
        return A * exp2(b2, s2)(r) * (b2**2 * ln(b1, s1)(r) - 2 * b2 / (r + s1) - 1 / (r + s1)**2) 
    return f


def newton_gravity_potential(G, cutoff):
    def f(r):
        return G / np.where(r >= cutoff, r, cutoff)
    return f


def newton_gravity_force(G, cutoff):
    def f(r):
        return -G / np.where(r >= cutoff, r, cutoff)**2
    return f


def newton_gravity_force_derivative(G, cutoff):
    def f(r):
        return 2 * G / np.where(r >= cutoff, r, cutoff)**3
    return f


def newton_iteration(func, derivative, initial_value, tolerance=0.01, max_steps=1000):
    zero = initial_value
    new_zero = None
    for i_step in range(0, max_steps):
        new_zero = zero - func(zero) / derivative(zero)

        if np.abs(new_zero - zero) < tolerance:
            break
        else:
            zero = new_zero

        if i_step >= max_steps:
            raise ValueError("Newton iteration did not converge")

    return new_zero
