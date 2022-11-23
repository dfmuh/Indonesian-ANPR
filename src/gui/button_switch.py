import tkinter as tk

class ButtonSwitch(tk.Frame):
    def __init__(self, parent, background):
        tk.Frame.__init__(self, parent)
        self.background = background
        self.on = tk.PhotoImage(file='../src/resources/images/toggleSwitch_On.png')
        self.off = tk.PhotoImage(file='../src/resources/images/toggleSwitch_Off.png')
        self.is_off = True
        self.btn = tk.Button(self, image=self.off, bd=0, bg=self.background, relief='sunken',
                             activebackground=background, command=self.clicked)
        self.btn.grid(row=0, column=0)

    def clicked(self):
        if self.is_off:
            self.btn.configure(image=self.on)
            self.is_off = False
        else:
            self.btn.configure(image=self.off)
            self.is_off = True