class Processor:
    def __init__(self, stages, thrust, mass, burn_rate, burn_time, h):
        self.g = 9.8
        self.stages = stages

        self.mass = mass
        self.thrust = [i * 1000 for i in thrust]  # 153.51 * 1000  # kN
        self.initial_mass = sum(mass)  # 3380  # kg
        self.burn_rate = burn_rate  # 87.37864  # kg / s
        self.burn_time = burn_time  # 10.3  # s

        self.specific_impulse = [self.thrust[i] / (self.g * self.burn_rate[i]) for i in range(self.stages)]  # s
        self.drag_coefficient = 0.38  # kg / m

        self.final_mass = [self.initial_mass - self.burn_time[i] * self.burn_time[i] for i in range(stages)]
        self.h = h  # 0.5

    @staticmethod
    def m_t(mass, time, lamb):
        return mass - time*lamb

    def v_t(self, r, m, lam, t, g, k, v):
        return (r - g * self.m_t(m, t, lam) - k * v * v + lam * v) / self.m_t(m, t, lam)
