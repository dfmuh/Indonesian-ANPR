from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
from src.assets.update_db import *

"""Open functions."""
def open_img(self):
    delete_img(self)
    import cv2

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Capture Image")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capture Image", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame.png"
            cv2.imwrite("../Image/" + img_name, frame)
            print("{} written!".format(img_name))
            self.file_img = "../Image/" + img_name

    if len(self.file_img) > 0:
        self.lbl_f_path.configure(text=self.file_img)
        img = cv2.imread(self.file_img)
        self.update_img(img)

    cam.release()

    cv2.destroyAllWindows()

"""Render functions."""

def refresh_img(self):
    delete_img(self)
    self.lbl_f_path.configure(text=self.file_img)
    img = cv2.imread(self.file_img)
    self.update_img(img)

def delete_img(self):
    if self.cap is not None:
        self.cap.release()
        self.cap = None
    self.lbl_f_path.configure(text="Any file is not opened")
    self.lbl_img.imgtk = ""

def num_of_it(self):
    self.number = len(self.cnt)
    self.lbl_num.destroy()
    self.lbl_num = tk.Label(self, width=8, bg='white', font=('Arial', 12), text=int(self.number))
    self.lbl_num.place(x=480, y=621)

def num_plate(self):
    self.lbl_num.destroy()
    self.number = self.text.replace(" ", "").replace("[", "").replace("]", "").replace(".", "").replace("(", "").replace(")", "")
    self.lbl_num = tk.Label(self, width=12, bg='white', font=('Arial', 12), text=self.number)
    self.lbl_num.place(x=440, y=621)
    return self.number

def open_db_np(self):
    self.db = UpdateDB()

def check_db_np(self):
    db = PlateNum_DB('../src/resources/num_plate_db/num_plates.db')
    plate_info = db.read_one(self.number)
    messagebox.showinfo("Number Plate", plate_info)

