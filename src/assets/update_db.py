import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from src.assets.data_base import PlateNum_DB
from src.assets.commands import *

class UpdateDB():
    def __init__(self):
        """Window."""
        self.window = tk.Tk()
        self.window.geometry('300x200')
        self.window.title("The Number Plates DB")
        """Data Base."""
        self.db = PlateNum_DB('../src/resources/num_plate_db/num_plates.db')
        """Coordinates."""
        sep = 25
        lbl_x = 10
        lbl_y = 20
        e_x = 140
        e_y = 20
        """Labels."""
        lbl_date = tk.Label(self.window, text='Date of Registration', font=("Arial", 10))
        lbl_date.place(x=lbl_x, y=lbl_y)
        lbl_number = tk.Label(self.window, text='Plate Number', font=("Arial", 10))
        lbl_number.place(x=lbl_x, y=lbl_y + sep)
        lbl_city = tk.Label(self.window, text='City', font=("Arial", 10))
        lbl_city.place(x=lbl_x, y=lbl_y + sep * 2)
        lbl_first_name = tk.Label(self.window, text='First Name', font=("Arial", 10))
        lbl_first_name.place(x=lbl_x, y=lbl_y + sep * 3)
        lbl_second_name = tk.Label(self.window, text='Second Name', font=("Arial", 10))
        lbl_second_name.place(x=lbl_x, y=lbl_y + sep * 4)
        """Entry Spaces."""
        self.e_date = DateEntry(self.window, selectmode='day', width=20, date_pattern='yyyy-mm-dd')
        self.e_date.place(x=e_x, y=e_y)
        self.e_number = tk.Entry(self.window, width=23, bd=1)
        self.e_number.place(x=e_x, y=e_y + sep)
        self.e_city = tk.Entry(self.window, width=23, bd=1)
        self.e_city.place(x=e_x, y=e_y + sep * 2)
        self.e_first_name = tk.Entry(self.window, width=23, bd=1)
        self.e_first_name.place(x=e_x, y=e_y + sep * 3)
        self.e_second_name = tk.Entry(self.window, width=23, bd=1)
        self.e_second_name.place(x=e_x, y=e_y + sep * 4)
        """Buttons."""
        btn_db = tk.Button(self.window, text='DataBase', command=self.data_base)
        btn_db.place(x=75, y=170)
        btn_submit = tk.Button(self.window, text='Submit', command=self.submit)
        btn_submit.place(x=135, y=170)
        btn_delete = tk.Button(self.window, text='Delete', command=self.delete_data)
        btn_delete.place(x=185, y=170)

    """Commands."""
    def submit(self):
        date = self.e_date.get()
        if len(self.e_number.get()) in range(5, 20) and len(self.e_city.get()) > 2 \
                and len(self.e_first_name.get()) > 2 and len(self.e_second_name.get()) > 2:
            number = self.e_number.get().upper()
            city = self.e_city.get().upper()
            first = self.e_first_name.get().upper()
            second = self.e_second_name.get().upper()
            if number.isalnum() and city.isalpha() and first.isalpha() and second.isalpha():
                item = (date, number, city, first, second)
                self.db.insert(item)
                messagebox.showinfo("Info", date + " " + number + " " + city + " " + first + " " + second +
                                    "\n\nAdd to Data Base")
        else:
            messagebox.showerror("Error", "The Wrong Information!\nPlease, Insert Your information in the correct" +
                                 "form!\nThe field Plate Number must contain only letters and numbers!\nOther " +
                                 "fields must contain only letters!\n\n")

    def data_base(self):
        text = self.db.read_all()
        messagebox.showinfo("All Number Plates in DB", text)

    def delete_data(self):
        number = self.e_number.get()
        self.db.delete_one(number)
        messagebox.showinfo("WARNING!", f"The Information about of the Number Plate {number} has been deleted!")









