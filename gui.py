from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import forward_euler
import backward_euler
import trapezoid
import runge_kutta


class StepInput(Frame):
    def __init__(self, frame, num):
        super(StepInput, self).__init__(frame)
        Label(frame, text=f'{num} stage').grid(column=0 + 2*num, row=0, columnspan=2)
        Label(frame, text='Thrust').grid(column=0 + 2*num, row=1)
        self.thrust_entry = Entry(frame).grid(column=1 + 2*num, row=1)
        Label(frame, text='Mass').grid(column=0 + 2*num, row=2)
        self.mass_entry = Entry(frame).grid(column=1 + 2*num, row=2)
        Label(frame, text='Fuel mass').grid(column=0 + 2*num, row=3)
        self.fuel_mass_entry = Entry(frame).grid(column=1 + 2*num, row=3)
        Label(frame, text='Burn rate').grid(column=0 + 2*num, row=4)
        self.burn_rate_entry = Entry(frame).grid(column=1 + 2*num, row=4)


class Application(Frame):

    def update_steps(self, event):
        print(self.number_of_steps.get())

    def __init__(self, window):
        super(Application, self).__init__(window)

        self.window = window

        self.steps = []

        self.method_name = [
                            'Forward Euler',
                            'Backward Euler',
                            'Trapezoid',
                            'Runge-Kutta',
                            ]

        self.method_executor = [
                                forward_euler.ForwardEuler().compute,
                                backward_euler.BackwardEuler().compute,
                                trapezoid.Trapezoid().compute,
                                runge_kutta.RungeKutta().compute,
                                ]

        self.method = dict(zip(self.method_name, self.method_executor))
        # print(self.method)

        self.upper_frame = Frame(self.window)
        self.upper_frame.pack()

        Label(self.upper_frame, text='Steps').grid(column=0, row=0)
        self.number_of_steps = ttk.Combobox(self.upper_frame,
                                            values=[1, 2, 3],
                                            state='readonly')
        self.number_of_steps.bind("<<ComboboxSelected>>", self.update_steps)
        self.number_of_steps.current(0)
        self.number_of_steps.grid(column=0, row=1)

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

        self.step_input_button = Button(self.upper_frame, text='Configure', command=self.tmp_configure)
        self.step_input_button.grid(column=4, row=0)

        self.evaluate_button = Button(self.upper_frame, text="Evaluate", command=self.evaluate, state=DISABLED)
        self.evaluate_button.grid(column=4, row=1)

        # ----------------
        self.step_input_frame = Frame(self.window)
        self.step_input_frame.pack()
        # ----------------

        self.graph_frame = Frame(self.window)
        self.graph_frame.pack()

    def tmp_configure(self):
        self.number_of_steps['state'] = DISABLED
        self.method_chooser['state'] = DISABLED
        self.step_chooser['state'] = DISABLED
        self.step_input_button['state'] = DISABLED

        self.evaluate_button['state'] = NORMAL

        for i in range(int(self.number_of_steps.get())):
            self.steps.append(StepInput(frame=self.step_input_frame, num=i).grid(column=i, row=0))

    def evaluate(self):

        steps, v = self.method[self.method_chooser.get()]()

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(range(steps), v, 'b-')
        a.set_title(f'{self.method_chooser.get()} method')
        a.set_xlabel('Time, s')
        a.set_ylabel('Velocity, m/s')
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()
