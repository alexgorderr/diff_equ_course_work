import math
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import forward_euler
import backward_euler
import heun
import runge_kutta


class StageInput(Frame):
    def __init__(self, app, frame, num):
        super(StageInput, self).__init__(frame)

        Label(frame, text=f'{num+1} stage').grid(column=0 + 2*num, row=0, columnspan=2)
        Label(frame, text='Thrust, kN').grid(column=0 + 2*num, row=1)
        self.thrust_entry = Entry(frame)
        self.thrust_entry.grid(column=1 + 2*num, row=1)
        app.thrust_entry.append(self.thrust_entry)

        Label(frame, text='Mass, kg').grid(column=0 + 2*num, row=2)
        self.mass_entry = Entry(frame)
        self.mass_entry.grid(column=1 + 2*num, row=2)
        app.mass_entry.append(self.mass_entry)

        Label(frame, text='Burn rate, kg/s').grid(column=0 + 2*num, row=3)
        self.burn_rate_entry = Entry(frame)
        self.burn_rate_entry.grid(column=1 + 2*num, row=3)
        app.burn_rate_entry.append(self.burn_rate_entry)

        Label(frame, text='Burn time, s').grid(column=0 + 2*num, row=4)
        self.burn_time_entry = Entry(frame)
        self.burn_time_entry.grid(column=1 + 2 * num, row=4)
        app.burn_time_entry.append(self.burn_time_entry)
    

class Application(Frame):

    def __init__(self, window):
        super(Application, self).__init__(window)
        window.title = 'CW'
        self.window = window

        self.stages = []

        self.thrust_entry = []
        self.mass_entry = []
        self.burn_rate_entry = []
        self.burn_time_entry = []

        self.method_name = [
            'Forward Euler',
            'Backward Euler',
            'Heun',
            'Runge-Kutta',
        ]

        self.upper_frame = Frame(self.window)
        self.upper_frame.pack()

        Label(self.upper_frame, text='Stages').grid(column=0, row=0)
        self.number_of_stages = ttk.Combobox(self.upper_frame,
                                             values=[1, 2, 3],
                                             state='readonly')
        self.number_of_stages.bind("<<ComboboxSelected>>", self.conf_stages)
        self.number_of_stages.current(0)
        self.number_of_stages.grid(column=0, row=1)

        Label(self.upper_frame, text='Method').grid(column=1, row=0)
        self.method_chooser = ttk.Combobox(self.upper_frame,
                                           values=self.method_name,
                                           state='readonly')
        self.method_chooser.current(0)
        self.method_chooser.grid(column=1, row=1)

        Label(self.upper_frame, text='h').grid(column=2, row=0)
        self.step_chooser = ttk.Combobox(self.upper_frame,
                                         values=[1, 0.75, 0.5, 0.25],
                                         state='readonly')
        self.step_chooser.current(2)
        self.step_chooser.grid(column=2, row=1)

        self.evaluate_button = Button(self.upper_frame, text="Evaluate", command=self.evaluate, state=DISABLED)
        self.evaluate_button.grid(column=4, row=0, rowspan=2)

        # ----------------
        self.stages_input_frame = Frame(self.window)
        self.stages_input_frame.pack()
        # ----------------

        self.graph_frame = Frame(self.window)
        self.graph_frame.pack()

    def conf_stages(self, event):
        self.evaluate_button['state'] = NORMAL

        while len(self.stages) > int(self.number_of_stages.get()):
            break

        for i in range(len(self.stages), int(self.number_of_stages.get())):
            self.stages.append(StageInput(self, frame=self.stages_input_frame, num=i))
            self.stages[i].grid(column=i, row=0)

    def evaluate(self):
        # thrust = [float(i.get()) for i in self.thrust_entry]
        # mass = [int(i.get()) for i in self.mass_entry]
        # burn_rate = [float(i.get()) for i in self.burn_rate_entry]
        # burn_time = [float(i.get()) for i in self.burn_time_entry]
        stages = int(self.number_of_stages.get())
        h = float(self.step_chooser.get())

        thrust = [153.51, 120]
        mass = [3380, 2200]
        burn_rate = [87.37864, 87.37864 / 2]
        burn_time = [10.3, 10.3 / 2]

        thrust = [153.51]
        mass = [3380]
        burn_rate = [87.37864]
        burn_time = [10.3]

        method_executor = [
            forward_euler.ForwardEuler(stages, thrust, mass, burn_rate, burn_time, h).compute,
            backward_euler.BackwardEuler(stages, thrust, mass, burn_rate, burn_time, h).compute,
            heun.Heun(stages, thrust, mass, burn_rate, burn_time, h).compute,
            runge_kutta.RungeKutta(stages, thrust, mass, burn_rate, burn_time, h).compute,
        ]

        method = dict(zip(self.method_name, method_executor))
        # print(self.method)

        t, v, v_ = method[self.method_chooser.get()]()

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        x = [h * i for i in range(t)]
        y1 = v
        y2 = v_
        a.plot(x, y1, 'b-')
        a.plot(x, y2, 'g-')
        a.plot(x, [abs(y1[i]-y2[i]) for i in range(len(x))], 'r-', )
        a.set_title(f'{self.method_chooser.get()} method')
        a.set_xlabel('Time, s')
        a.set_ylabel('Velocity, m/s')
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)

        if len(canvas.get_tk_widget().master.children) > 1:
            list(canvas.get_tk_widget().master.children.values())[0].destroy()

        canvas.get_tk_widget().pack()
        canvas.draw()
