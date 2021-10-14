from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import forward_euler
import backward_euler
import runge_kutta
import heun


class Application:

    def __init__(self, window):

        self.window = window

        self.method_name = ['Forward Euler',
                            'Backward Euler',
                            'Runge-Kutta',
                            'Heun']

        self.method_executor = [forward_euler.ForwardEuler().compute,
                                backward_euler.BackwardEuler().compute,
                                runge_kutta.RungeKutta().compute,
                                heun.Heun().compute]

        self.method = dict(zip(self.method_name, self.method_executor))
        print(self.method)

        self.upper_frame = Frame(self.window)
        self.upper_frame.pack()

        Label(self.upper_frame, text='Steps').grid(column=0, row=0)
        self.number_of_steps = ttk.Combobox(self.upper_frame,
                                            values=[1, 2, 3, 4],
                                            state='readonly')
        self.number_of_steps.current(0)
        self.number_of_steps.grid(column=0, row=1)

        Label(self.upper_frame, text='Method').grid(column=1, row=0)
        self.method_chooser = ttk.Combobox(self.upper_frame,
                                           values=['Forward Euler',
                                                   'Backward Euler',
                                                   'Runge-Kutta',
                                                   'Heun'],
                                           state='readonly')
        self.method_chooser.current(0)
        self.method_chooser.grid(column=1, row=1)

        Label(self.upper_frame, text='h').grid(column=2, row=0)
        self.step_chooser = ttk.Combobox(self.upper_frame,
                                         values=[1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001],
                                         state='readonly')
        self.step_chooser.current(2)
        self.step_chooser.grid(column=2, row=1)

        self.step_input_button = Button(self.upper_frame, text='Configure', command=self.configure)
        self.step_input_button.grid(column=4, row=0, rowspan=2)
        # ----------------
        self.step_input = Frame(self.window)
        self.step_input.pack()

        self.evaluate_button = Button(self.step_input, text="Evaluate", command=self.evaluate, state=DISABLED)
        self.evaluate_button.grid(column=4, row=0, rowspan=2)

        self.graph_frame = Frame(self.window)
        self.graph_frame.pack()

    def configure(self):
        self.number_of_steps['state'] = DISABLED
        self.method_chooser['state'] = DISABLED
        self.step_chooser['state'] = DISABLED
        self.step_input_button['state'] = DISABLED

        self.evaluate_button['state'] = NORMAL

        for i in range(int(self.number_of_steps.get())):
            print('!!!')
            # elem.grid(column=i, row=0)

    def evaluate(self):

        steps, v = self.method[self.method_chooser.get()]()

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(range(steps), v, 'b-')
        a.set_title('Euler method')
        a.set_xlabel('Time, s')
        a.set_ylabel('Velocity, m/s')
        # self.graph_frame.master.children.pop()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()
