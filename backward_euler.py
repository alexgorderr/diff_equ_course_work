from processor import Processor


class BackwardEuler(Processor):
    def compute(self):
        v = [0]
        steps = int(round(self.engine_burn / self.h, 0))
        for n in range(1, steps):
            v.append(v[-1] + self.h * self.v_t(self.thrust,
                                               self.initial_mass,
                                               self.consumption_rate, n+1, self.g,
                                               self.drag_coefficient, v[-1]))
            print(f"Step: {n}, Xn: {n * self.h}, Vn: {v[-1]}")
        return steps, v
