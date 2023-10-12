import os
import shutil
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from api import DNNTest

dnnTest = DNNTest("DNNTesting")


class ImageDetectionPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.image_detection_window = None
        self.model_path = ""
        self.image_detection_page()

    def image_detection_page(self):
        # Creating a new Tkinter window
        self.image_detection_window = tk.Toplevel(self.master)
        self.image_detection_window.title("Object Detection On Image")

        # Create the left section for image selection
        image_frame = tk.Frame(self.image_detection_window)
        image_frame.pack(side=tk.LEFT)

        # Create the "Select Image" button
        def browse_image():
            filepath = filedialog.askopenfilename()
            if filepath:
                self._display_image(self.image_label, filepath)
                self._hide_image(self.detection_result_image)

        select_button = tk.Button(image_frame, text="Select Image", command=browse_image)
        select_button.pack()

        # Create a label to display the selected image
        self.image_label = tk.Label(image_frame, width=50, height=20, borderwidth=2, relief="groove")
        self.image_label.pack()

        # Create the right section for model detection
        model_frame = tk.Frame(self.image_detection_window)
        model_frame.pack(side=tk.RIGHT)

        model_selection_frame = tk.Frame(model_frame)
        model_selection_frame.pack(side=tk.TOP)

        from util import update_readonly_textbox

        def browse_label_path():
            filepath = filedialog.askopenfilename(initialdir="./MetaHand/tools/yolov7/runs/train")
            self.model_path = filepath
            update_readonly_textbox(self.model_path_box, filepath)

        model_path_frame = tk.Frame(model_selection_frame)
        model_path_frame.pack(side=tk.LEFT)
        self.model_path_button = tk.Button(model_path_frame, text="Select Original Model",
                                           command=browse_label_path)
        self.model_path_button.pack(side=tk.LEFT)
        self.model_path_box = tk.Text(model_path_frame, height=1, width=20)
        self.model_path_box.pack(side=tk.LEFT)

        detect_button = tk.Button(model_path_frame, text="DETECT", command=self.detect)
        detect_button.pack(side=tk.LEFT)

        # Create the image display frame
        self.detection_result_image = tk.Label(model_frame, width=50, height=20, relief="groove", borderwidth=2)
        self.detection_result_image.pack(side=tk.BOTTOM)

    @staticmethod
    def _load_model(dest_dir="./MetaHand/tools/yolov7/runs/train"):
        model_list = []
        for model_name in os.listdir(dest_dir):
            model_list.append(os.path.splitext(model_name)[0])
        return model_list

    def detect(self, dest_dir="./MetaHand/tools/yolov7/runs/train"):
        if not hasattr(self.image_label, "image") and not hasattr(self.image_label, "text"):
            raise ValueError("You should pick image fist!")
        image_path = self.image_label.text
        model_path = "./runtime/weights.pt"
        if "tools/yolov7/" in self.model_path:
            model_path = "./MetaHand/tools/yolov7/" + self.model_path.split("/tools/yolov7/")[-1]
        else:
            shutil.copy(self.model_path, model_path)
        weights_path = os.path.join("/root", model_path)
        tmp_img_path = "./tmp/temp.jpg"
        os.makedirs("./tmp", exist_ok=True)
        shutil.copy(image_path, tmp_img_path)
        res = dnnTest.detect_yolov7(img_path="/root/tmp/temp.jpg", weights_path=weights_path)
        self.show_detection_result(img_path=res)

    @staticmethod
    def _display_image(image_label: tk.Label, filepath: str):
        # Display the selected image
        image = Image.open(filepath)
        # Resize the image to fit within the label without changing its aspect ratio
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo, width=400, height=400, text=filepath)
        image_label.image = photo
        image_label.text = filepath

    @staticmethod
    def _hide_image(image_label: tk.Label):
        if hasattr(image_label, "image"):
            del image_label.image

    def show_detection_result(self, img_path):
        self._display_image(self.detection_result_image, img_path)
