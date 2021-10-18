class Processor:
    def __init__(self):  # , thrusts, engine_burn, consumption_rate, rocket_mass, fuel_mass):
        self.g = 9.8

        self.thrust = 153.51 * 1000  # kN
        self.engine_burn = 10.3  # s
        self.consumption_rate = 87.37864  # kg / s
        self.initial_mass = 3380  # kg

        self.specific_impulse = self.thrust / (self.g * self.consumption_rate)  # s
        self.drag_coefficient = 0.38  # kg / m

        self.final_mass = self.initial_mass - self.engine_burn * self.consumption_rate
        self.h = 0.5

    @staticmethod
    def m_t(mass, time, lamb):
        return mass - time*lamb

    def v_t(self, r, m, lam, t, g, k, v):
        return (r - g * self.m_t(m, t, lam) - k * v * v + lam * v) / self.m_t(m, t, lam)

