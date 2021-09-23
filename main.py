"""
    Euler method integrated in GUI
"""

import numpy as np
import matplotlib
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Application:

    def __init__(self, window):
        self.window = window
        self.button = Button(window, text="Evaluate", command=self.evaluate)
        self.button.pack()

        self.g = 9.8
        self.thrust = 153.51 * 1000  # kN
        self.engine_burn = 10.3  # s
        self.specific_impulse = 179.1  # s
        self.drag_coefficient = 0.38  # kg / m
        self.consumption_rate = 87.37864  # kg / s

        self.initial_mass = 3380  # kg
        self.final_mass = self.initial_mass - self.engine_burn * self.consumption_rate

        self.h = 0.5

    def m_t(self, mass, time, lamb):
        return mass - time*lamb

    def v_t(self, r, m, lam, t, g, k, v):
        return (r - g * self.m_t(m, t, lam) - k * v * v + lam * v) / self.m_t(m, t, lam)

    def evaluate(self):
        v = [0]

        steps = int(round(self.engine_burn / self.h, 0))

        for n in range(1, steps):
            v.append(v[-1] + self.h * self.v_t(self.thrust,
                                      self.initial_mass,
                                      self.consumption_rate, n, self.g,
                                      self.drag_coefficient, v[-1]))
            print(f"Step: {n}, Xn: {n * self.h}, Vn: {v[-1]}")
        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(range(steps), v, 'b-')
        a.set_title('Euler method')
        a.set_xlabel('Time, s')
        a.set_ylabel('Velocity, m/s')
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()


if __name__ == '__main__':
    window = Tk()
    app = Application(window)
    window.mainloop()
