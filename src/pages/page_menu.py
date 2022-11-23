import tkinter as tk


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3F72AF')
        self.controller = controller

        """Title."""
        lbl_ttl = tk.Label(self, text="Automatic Number-Plate Recognition", font=("Arial Bold", 30), bg='#3F72AF',
                           fg='white')
        lbl_ttl.place(x=75, y=125)

        """Buttons."""
        btn_anpr = tk.Button(self, text="Start", width=10, command=lambda: controller.up_frame('ANPR'))
        btn_anpr.place(x=388, y=250)

        # btn_quit = tk.Button(text='Quit', width=10, command=lambda: controller.up_frame('QUIT'))
        # btn_quit.place(x=390, y=130)
