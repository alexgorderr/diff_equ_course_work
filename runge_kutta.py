import math
from processor import Processor


class RungeKutta(Processor):
    def compute(self):
        sum_steps = 1
        v = [0]
        v_ = [0]
        mass = self.initial_mass
        for i in range(self.stages):
            steps = int(round(self.burn_time[i] / self.h, 0))
            for n in range(steps):
                k1 = self.v_t(self.thrust[i],
                              mass,
                              self.burn_rate[i], n, self.g,
                              self.drag_coefficient, v[-1])
                k2 = self.v_t(self.thrust[i],
                              mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k1 * self.h/2)
                k3 = self.v_t(self.thrust[i],
                              mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k2 * self.h/2)
                k4 = self.v_t(self.thrust[i],
                              mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k3 * self.h/2)
                v.append(v[-1] + (self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
                v_.append(self.specific_impulse[i] * self.g * n * math.log(mass / self.m_t(mass, n, self.burn_rate[i])))
                print(f"Step: {sum_steps+n}, Xn: {sum_steps+n-1 * self.h}, Vn: {v[-1]}")
            sum_steps += steps
            mass -= self.mass[i]
        return sum_steps, v, v_
