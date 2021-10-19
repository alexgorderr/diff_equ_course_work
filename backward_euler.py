from processor import Processor


class BackwardEuler(Processor):
    def compute(self):
        sum_steps = 1
        v = [0]
        for i in range(self.stages):
            steps = int(round(self.burn_time[i] / self.h, 0))
            for n in range(steps):
                v.append(v[-1] + self.h * self.v_t(self.thrust[i],
                                                   self.initial_mass,
                                                   self.burn_rate[i], n+1, self.g,
                                                   self.drag_coefficient, v[-1]))
                print(f"Step: {sum_steps+n}, Xn: {sum_steps+n * self.h}, Vn: {v[-1]}")
            sum_steps += steps
        return sum_steps, v
