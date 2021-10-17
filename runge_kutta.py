from processor import Processor


class RungeKutta(Processor):
    def compute(self):
        v = [0]
        steps = int(round(self.engine_burn / self.h, 0))
        for n in range(1, steps):
            k1 = self.v_t(self.thrust,
                          self.initial_mass,
                          self.consumption_rate, n, self.g,
                          self.drag_coefficient, v[-1])
            k2 = self.v_t(self.thrust,
                          self.initial_mass,
                          self.consumption_rate, n + self.h/2, self.g,
                          self.drag_coefficient, v[-1] + k1 * self.h/2)
            k3 = self.v_t(self.thrust,
                          self.initial_mass,
                          self.consumption_rate, n + self.h/2, self.g,
                          self.drag_coefficient, v[-1] + k2 * self.h/2)
            k4 = self.v_t(self.thrust,
                          self.initial_mass,
                          self.consumption_rate, n + self.h/2, self.g,
                          self.drag_coefficient, v[-1] + k3 * self.h/2)
            v.append(v[-1] + (self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
            print(f"Step: {n}, Xn: {n * self.h}, Vn: {v[-1]}")
        return steps, v
