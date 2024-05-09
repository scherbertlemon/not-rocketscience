import numpy as np


def exp2(b_2, s_2):
    def f(x):
        return np.exp(-b_2 * (x - s_2))
    return f


def ln(b_1, s_1):
    def f(x):
        return np.log(b_1 * (x + s_1))
    return f


def combination(A, b_1, s_1, b_2, s_2):
    def f(x):
        return A * ln(b_1, s_1)(x) * exp2(b_2, s_2)(x)
    return f


def deriv_combination(A, b_1, s_1, b_2, s_2):
    def f(x):
        return A * exp2(b_2, s_2)(x) * (1/(x + s_1) - b_2 * ln(b_1, s_1)(x))
    return f


def newton_gravity(r, min_r=0.2):
    return -100 / r**2 if r > min_r else -100 / min_r**2