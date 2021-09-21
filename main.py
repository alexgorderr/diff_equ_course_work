"""
    Euler method
"""

import numpy as np
import matplotlib.pyplot as plt

g = 9.8
thrust = 153.51 * 1000  # kN
engine_burn = 10.3  # s
specific_impulse = 179.1  # s
drag_coefficient = 0.38  # kg / m
consumption_rate = 87.37864  # kg / s

initial_mass = 3380  # kg
final_mass = initial_mass - engine_burn * consumption_rate


def m_t(mass, time, lamb):
    return mass - time*lamb


def v_t(r, m, lam, t, g, k, v):
    return (r - g * m_t(m, t, lam) - k * v * v + lam * v) / m_t(m, t, lam)


v = [0]
h = 0.5
steps = int(round(engine_burn / h, 0))
for n in range(1, steps):
    v.append(v[-1] + h*v_t(thrust, initial_mass, consumption_rate, n, g, drag_coefficient, v[-1]))
    # print(f"Step: {n}, Xn: {n*h}, Vn: {v[-1]}")

plt.plot(range(steps), v)
plt.xticks(x=steps)
plt.xlabel('Time, s')
plt.ylabel('Velocity, m/s')
plt.show()
