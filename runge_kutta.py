from processor import Processor


class RungeKutta(Processor):
    def compute(self):
        sum_steps = 1
        v = [0]
        for i in range(self.stages):
            steps = int(round(self.burn_time[i] / self.h, 0))
            for n in range(steps):
                k1 = self.v_t(self.thrust[i],
                              self.initial_mass,
                              self.burn_rate[i], n, self.g,
                              self.drag_coefficient, v[-1])
                k2 = self.v_t(self.thrust[i],
                              self.initial_mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k1 * self.h/2)
                k3 = self.v_t(self.thrust[i],
                              self.initial_mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k2 * self.h/2)
                k4 = self.v_t(self.thrust[i],
                              self.initial_mass,
                              self.burn_rate[i], n + self.h/2, self.g,
                              self.drag_coefficient, v[-1] + k3 * self.h/2)
                v.append(v[-1] + (self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
                print(f"Step: {sum_steps+n}, Xn: {sum_steps+n-1 * self.h}, Vn: {v[-1]}")
            sum_steps += steps
        return sum_steps, v
