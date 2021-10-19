import math
from processor import Processor


class ForwardEuler(Processor):
    def compute(self):
        sum_steps = 1
        v = [0]
        v_ = [0]
        mass = self.initial_mass
        for i in range(self.stages):
            steps = int(round(self.burn_time[i] / self.h, 0))
            for n in range(steps):
                v.append(v[-1] + self.h * self.v_t(self.thrust[i],
                                                   mass,
                                                   self.burn_rate[i], n, self.g,
                                                   self.drag_coefficient, v[-1]))
                print(f"Step: {sum_steps+n}, Xn: {sum_steps+n * self.h}, Vn: {v[-1]}")
                v_ = []
            sum_steps += steps
            mass -= self.mass[i]
        return sum_steps, v, v_
