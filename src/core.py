import tkinter as tk

from src.pages.page_menu import Menu
from src.pages.page_anpr import ANPR


class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, minsize=680)
        container.grid_columnconfigure(0, minsize=860)

        self.listing = {}

        for p in (Menu, ANPR):
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.listing[page_name] = frame

        self.up_frame('Menu')

    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()


if __name__ == "__main__":
    app = Core()
    app.geometry('860x680')
    app.title('ANPR')
    app.iconbitmap('../src/resources/images/webcam.ico')
    app.resizable(0, 0)
    app.mainloop()
