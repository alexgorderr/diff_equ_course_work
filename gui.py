from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import forward_euler
import backward_euler
import heun
import runge_kutta


class StageInput(Frame):
    def __init__(self, frame, num):
        super(StageInput, self).__init__(frame)
        Label(frame, text=f'{num+1} stage').grid(column=0 + 2*num, row=0, columnspan=2)
        Label(frame, text='Thrust').grid(column=0 + 2*num, row=1)
        self.thrust_entry = Entry(frame).grid(column=1 + 2*num, row=1)
        Label(frame, text='Mass').grid(column=0 + 2*num, row=2)
        self.mass_entry = Entry(frame).grid(column=1 + 2*num, row=2)
        Label(frame, text='Fuel mass').grid(column=0 + 2*num, row=3)
        self.fuel_mass_entry = Entry(frame).grid(column=1 + 2*num, row=3)
        Label(frame, text='Burn rate').grid(column=0 + 2*num, row=4)
        self.burn_rate_entry = Entry(frame).grid(column=1 + 2*num, row=4)
        Label(frame, text='Burn time').grid(column=0 + 2*num, row=5)
        self.burn_time_entry = Entry(frame).grid(column=1 + 2 * num, row=5)


class Application(Frame):

    def update_stages(self, event):
        print(self.number_of_stages.get())

    def __init__(self, window):
        super(Application, self).__init__(window)

        self.window = window

        self.stages = []

        self.method_name = [
            'Forward Euler',
            'Backward Euler',
            'Heun',
            'Runge-Kutta',
        ]

        args = []

        self.method_executor = [
            forward_euler.ForwardEuler().compute,
            backward_euler.BackwardEuler().compute,
            heun.Heun().compute,
            runge_kutta.RungeKutta().compute,
        ]

        self.method = dict(zip(self.method_name, self.method_executor))
        # print(self.method)

        self.upper_frame = Frame(self.window)
        self.upper_frame.pack()

        Label(self.upper_frame, text='Stages').grid(column=0, row=0)
        self.number_of_stages = ttk.Combobox(self.upper_frame,
                                             values=[1, 2, 3],
                                             state='readonly')
        self.number_of_stages.bind("<<ComboboxSelected>>", self.update_stages)
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
                                         values=[1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001],
                                         state='readonly')
        self.step_chooser.current(2)
        self.step_chooser.grid(column=2, row=1)

        Label(self.upper_frame, text='Rocket mass').grid(column=3, row=0)
        self.rocket_mass = Entry(self.upper_frame).grid(column=3, row=1)

        self.stages_input_button = Button(self.upper_frame, text='Configure', command=self.tmp_configure)
        self.stages_input_button.grid(column=4, row=0)

        self.evaluate_button = Button(self.upper_frame, text="Evaluate", command=self.evaluate, state=DISABLED)
        self.evaluate_button.grid(column=4, row=1)

        # ----------------
        self.stages_input_frame = Frame(self.window)
        self.stages_input_frame.pack()
        # ----------------

        self.graph_frame = Frame(self.window)
        self.graph_frame.pack()

    def tmp_configure(self):
        # self.number_of_stage['state'] = DISABLED
        # self.method_chooser['state'] = DISABLED
        # self.step_chooser['state'] = DISABLED
        self.stages_input_button['state'] = DISABLED

        self.evaluate_button['state'] = NORMAL

        for i in range(int(self.number_of_stages.get())):
            self.stages.append(StageInput(frame=self.stages_input_frame, num=i).grid(column=i, row=0, ipadx=10))

    def evaluate(self):

        t, v = self.method[self.method_chooser.get()]()

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(range(t), v, 'b-')
        a.set_title(f'{self.method_chooser.get()} method')
        a.set_xlabel('Time, s')
        a.set_ylabel('Velocity, m/s')
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)

        if len(canvas.get_tk_widget().master.children) > 1:
            list(canvas.get_tk_widget().master.children.values())[0].destroy()

        canvas.get_tk_widget().pack()
        canvas.draw()
