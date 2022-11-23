import easyocr
import numpy as np
from src.gui.button_switch import ButtonSwitch
from src.assets.interface import *
from src.assets.update_db import *
import os
import cv2
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util
import sys


class ANPR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3F72AF')
        self.controller = controller

        """Separators."""
        sep_y = 35
        sep_s = 50

        """Coordinates"""
        lbl_sw_x = 30
        lbl_sw_y = 130
        lbl_sl_x = 30
        lbl_sl_y = 350
        btn_sw_x = 110
        btn_sw_y = 125
        btn_y = 620
        sl_x = 30
        sl_y = 370

        """Labels."""
        # Title
        background = '#3F72AF'
        tk_interface(self, "Automatic Number-Plate Recognition", background)

        lbl_contour = tk.Label(self, text="Detect", font=("Arial", 10), bg=background, fg="white")
        lbl_contour.place(x=lbl_sw_x, y=lbl_sw_y + sep_y * 4)

        # Number Info
        self.number = ""
        self.lbl_num = tk.Label(self, width=12, bg='white', font=('Arial', 12), text=self.number)
        self.lbl_num.place(x=440, y=621)

        """Buttons."""
        btn_menu = tk.Button(self, text='Menu', command=lambda: controller.up_frame("Menu"))
        btn_menu.place(x=757, y=btn_y)
        btn_db = tk.Button(self, text='AddData', command=lambda: open_db_np(self))
        btn_db.place(x=279, y=btn_y)
        btn_check = tk.Button(self, text='Check', command=lambda: check_db_np(self))
        btn_check.place(x=336, y=btn_y)
        btn_num = tk.Button(self, text='Number', command=lambda: num_plate(self))
        btn_num.place(x=380, y=btn_y)

        """Toggle Switches."""

        self.btn_contour = ButtonSwitch(self, background)
        self.btn_contour.place(x=btn_sw_x, y=btn_sw_y + sep_y * 4)

    def update_img(self, frame):
        self.orig_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2_img = self.orig_img

        if self.btn_contour.is_off == False:
            """Cropping Image"""
            try:
                sys.path.append("D:/models/research/")
                sys.path.append("D:/models/research/object_detection/utils")
                sys.path.append("D:/models/research/slim")
                sys.path.append("D:/models/research/slim/nets")

                # Name of the directory containing the object detection module we're using
                MODEL_NAME = '../tf/plat_baru'
                IMAGE_NAME = '../Image/opencv_frame.png'

                # Grab path to current working directory
                CWD_PATH = os.getcwd()

                # Path to frozen detection graph .pb file, which contains the model that is used
                # for object detection.
                PATH_TO_CKPT = 'tf/plat_baru/frozen_inference_graph.pb'

                # Path to label map file
                PATH_TO_LABELS = os.path.join(CWD_PATH, 'tf/data', 'plat_map.pbtxt')

                # Path to image
                PATH_TO_IMAGE = IMAGE_NAME

                # Number of classes the object detector can identify
                NUM_CLASSES = 1

                # Load the label map.
                # Label maps map indices to category names, so that when our convolution
                # network predicts `5`, we know that this corresponds to `king`.
                # Here we use internal utility functions, but anything that returns a
                # dictionary mapping integers to appropriate string labels would be fine
                label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
                categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                            use_display_name=True)
                category_index = label_map_util.create_category_index(categories)

                # Load the Tensorflow model into memory.
                detection_graph = tf.Graph()
                with detection_graph.as_default():
                    od_graph_def = tf.GraphDef()
                    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                        serialized_graph = fid.read()
                        od_graph_def.ParseFromString(serialized_graph)
                        tf.import_graph_def(od_graph_def, name='')

                    sess = tf.Session(graph=detection_graph)

                # Define input and output tensors (i.e. data) for the object detection classifier

                # Input tensor is the image
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

                # Output tensors are the detection boxes, scores, and classes
                # Each box represents a part of the image where a particular object was detected
                detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                # Each score represents level of confidence for each of the objects.
                # The score is shown on the result image, together with the class label.
                detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

                # Number of objects detected
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # Load image using OpenCV and
                # expand image dimensions to have shape: [1, None, None, 3]
                # i.e. a single-column array, where each item in the column has the pixel RGB value
                image = cv2.imread(PATH_TO_IMAGE)
                image_expanded = np.expand_dims(image, axis=0)

                # Perform the actual detection by running the model with the image as input
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_expanded})

                # Draw the results of the detection (aka 'visulaize the results')

                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8,
                    min_score_thresh=0.60)

                cv2_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            except IndexError:
                raise messagebox.showerror("IndexError", "Can't be found the number plate contour")

            try:
                """Read Text from Image"""
                reader = easyocr.Reader(['en'], gpu=False)
                result = reader.readtext(cv2_img)
                top_left = [0.0]
                bottom_right = [0, 0]

                if (len(result) == 3):
                    top_left = tuple(result[1][0][0])
                    bottom_right = tuple(result[1][0][2])
                elif (len(result) == 4):
                    top_left = tuple(result[1][0][0])
                    bottom_right = tuple(result[2][0][2])
                elif (len(result) == 5):
                    top_left = tuple(result[1][0][0])
                    bottom_right = tuple(result[3][0][2])

                cropped_img = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                cv2.imwrite("../Image/cropped_img.jpg", cropped_img)

                results = reader.readtext(cropped_img)
                self.text = ""
                for i in range(len(results)):
                    self.text += results[i][-2]
                    self.text = self.text.replace(".", "")
                    self.number = self.text.replace(" ", "")

                cv2.putText(self.orig_img, self.number, (10, 20), 1, 2, (255, 0, 0), 2)
            except IndexError:
                raise messagebox.showerror("IndexError", "Can't be found the number plate contour")

        img = Image.fromarray(cv2_img)
        img = img.resize((599, 557), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(image=img)
        self.lbl_img = tk.Label(self, image=img_tk)
        self.lbl_img.imgtk = img_tk
        self.lbl_img.place(x=200, y=50)
