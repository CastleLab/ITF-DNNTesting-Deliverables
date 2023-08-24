import os
import shutil
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from api import DNNTest

dnnTest = DNNTest("DNNTesting")
CLEAR_LIST = []

class ImageMutationPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.image_mutation_window = None
        self.image_mutation_page()

    def entry_module(self, frame, default_entry_text, des):
        CLEAR_LIST.append(default_entry_text)
        label = tk.Label(frame, width=10, text=des)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=30)
        entry.insert(tk.END, default_entry_text)
        entry.bind("<FocusIn>", self.clear_entry)
        entry.bind("<FocusOut>", self.default_entry)
        entry.pack(side=tk.LEFT)
        return entry

    def clear_entry(self, event):
        if event.widget.get() in CLEAR_LIST:
            event.widget.delete(0, tk.END)

    def default_entry(self, event):
        if event.widget.get() == "":
            if event.widget == self.label_path_entry:
                event.widget.insert(tk.END, "Please enter the path of training labels")

    # Implementation of Image Mutation Section
    def image_mutation_page(self):
        # Creating a new Tkinter window
        self.image_mutation_window = tk.Toplevel(self.master)
        self.image_mutation_window.title("Image Mutation")

        # Create the left section for image selection
        image_frame = tk.Frame(self.image_mutation_window)
        image_frame.pack(side=tk.LEFT)

        # Create the "Select Image" button
        def browse_image():
            filepath = filedialog.askopenfilename()
            if filepath:
                self._display_image(self.image_label, filepath)
                self._hide_image(self.mutation_result_image)

        select_button = tk.Button(image_frame, text="Select Image", command=browse_image)
        select_button.pack()

        # Create a label to display the selected image
        self.image_label = tk.Label(image_frame, width=50, height=20, borderwidth=2, relief="groove")
        self.image_label.pack()

        label_selection_frame = tk.Frame(image_frame)
        label_selection_frame.pack(side=tk.TOP)
        self.label_path_entry: tk.Entry = self.entry_module(frame=label_selection_frame,
                                                            default_entry_text="Please enter the path of training labels",
                                                            des="Label path")

        # Create the right section for model detection
        model_frame = tk.Frame(self.image_mutation_window)
        model_frame.pack(side=tk.RIGHT)

        mutation_selection_frame = tk.Frame(model_frame)
        mutation_selection_frame.pack(side=tk.TOP)

        # Create the "Select Model" label and option button
        mutate_label = tk.Label(mutation_selection_frame, text="Select Mutation Operator:")
        mutate_label.pack(side=tk.LEFT)

        self.mutation_var = tk.StringVar()
        mutation_list = ["background", "object"]
        mutation_dropdown = tk.OptionMenu(mutation_selection_frame, self.mutation_var, *mutation_list)
        self.mutation_var.set(mutation_list[0])
        mutation_dropdown.pack(side=tk.LEFT)

        detect_button = tk.Button(mutation_selection_frame, text="MUTATE", command=self.mutate)
        detect_button.pack(side=tk.RIGHT)

        # Create the image display frame
        self.mutation_result_image = tk.Label(model_frame, width=50, height=20, relief="groove", borderwidth=2)
        self.mutation_result_image.pack(side=tk.BOTTOM)

    def mutate(self, dest_dir="./MetaHand/tools/yolov7/runs/train"):
        image_path = self.image_label.text
        label_path = self.label_path_entry.get()
        mt = self.mutation_var.get()

        tmp_img_path = "./tmp/temp.jpg"
        tmp_label_path = "./tmp/label.txt"
        os.makedirs("./tmp", exist_ok=True)
        shutil.copy(image_path, tmp_img_path)
        shutil.copy(label_path, tmp_label_path)

        res = dnnTest.mutate_image(file_or_directory="file", image_path=os.path.join("/root/", tmp_img_path),
                                   label_path=os.path.join("/root/", tmp_label_path), mutate_type=mt)
        res = os.path.join("./MetaHand/data_pilot_test/test_mutate",
                           f"ObjectGaussianMutation/object_gaussian_160_fixMutRatio_centerXY_09/label.jpg")
        self.show_mutation_result(img_path=res)

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

    def show_mutation_result(self, img_path):
        self._display_image(self.mutation_result_image, img_path)
