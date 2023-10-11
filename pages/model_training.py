import os
import shutil
import tkinter as tk
from tkinter import filedialog
import shutil

import yaml

from api import DNNTest
from util import update_readonly_textbox

dnnTest = DNNTest("DNNTesting")

CLEAR_LIST = []


class ModelTrainingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_train_window = None
        self.model_train_page()
        self.image_folder_path = ""
        self.label_folder_path = ""

    def _create_dataset_preparation_frame(self, ):
        dataset_preparation_frame = tk.Frame(self.model_train_window)
        dataset_preparation_frame.pack(side=tk.LEFT)

        def browse_image_path():
            folder_path = filedialog.askdirectory()
            self.image_folder_path = folder_path
            update_readonly_textbox(self.image_path_box, folder_path)

        def browse_label_path():
            folder_path = filedialog.askdirectory()
            self.label_folder_path = folder_path
            update_readonly_textbox(self.label_path_box, folder_path)

        image_selection_frame = tk.Frame(dataset_preparation_frame)
        image_selection_frame.pack(side=tk.TOP)
        self.image_path_button = tk.Button(image_selection_frame, text="Select Images",
                                           command=browse_image_path)
        self.image_path_button.pack(side=tk.LEFT)
        self.image_path_box = tk.Text(image_selection_frame, height=1, width=50)
        self.image_path_box.pack(side=tk.RIGHT)

        label_selection_frame = tk.Frame(dataset_preparation_frame)
        label_selection_frame.pack(side=tk.TOP)
        self.label_path_button = tk.Button(label_selection_frame, text="Select Labels",
                                           command=browse_label_path)
        self.label_path_button.pack(side=tk.LEFT)
        self.label_path_box = tk.Text(label_selection_frame, height=1, width=50)
        self.label_path_box.pack(side=tk.RIGHT)

        dataset_name_frame = tk.Frame(dataset_preparation_frame)
        dataset_name_frame.pack(side=tk.TOP)
        self.dataset_name_entry: tk.Entry = self.entry_module(frame=dataset_name_frame,
                                                              default_entry_text="Please enter the name of your dataset",
                                                              des="Dataset name")

        self.dataset_button = tk.Button(dataset_preparation_frame, text="Prepare Dataset",
                                        command=self.prepare_dataset)
        self.dataset_button.pack()

    def _create_model_train_frame(self):
        # Creating the "Selecting Dataset" section
        model_train_frame = tk.Frame(self.model_train_window)
        model_train_frame.pack(side=tk.LEFT)
        model_train_option_frame = tk.Frame(model_train_frame)
        model_train_option_frame.pack(side=tk.TOP)

        data_label = tk.Label(model_train_option_frame, text="Select Dataset:")
        data_label.pack(side=tk.LEFT)
        self.train_data_var = tk.StringVar()
        cfg_list = self._load_data()
        self.train_data_var.set(cfg_list[0])  # default value
        self.train_data_var.trace('w', self.show_data_cfg)
        self.data_menu = tk.OptionMenu(model_train_option_frame, self.train_data_var, *cfg_list)
        self.data_menu.pack(side=tk.LEFT)

        model_label = tk.Label(model_train_option_frame, text="Select Model:")
        model_label.pack(side=tk.LEFT)
        model_list = ["yolov7-tiny", "yolov7"]
        self.train_model_var = tk.StringVar()
        self.train_model_var.set("yolov7")
        self.model_menu = tk.OptionMenu(model_train_option_frame, self.train_model_var, *model_list)
        self.model_menu.pack(side=tk.LEFT)

        self.cfg_text = tk.Text(model_train_frame, height=5, width=50)
        self.cfg_text.pack()
        self.train_button = tk.Button(model_train_frame, text="Start Training",
                                      command=self.train_model)
        self.train_button.pack()
        # show_data_cfg()

    def show_data_cfg(self, *args):
        with open(os.path.join("./MetaHand/tools/yolov7/data/", f"{self.train_data_var.get()}.yaml"), "r") as file:
            data_hyp = yaml.load(file, Loader=yaml.FullLoader)
        data_cfg = f"train: {data_hyp['train']}\nval: {data_hyp['val']}\n"
        update_readonly_textbox(self.cfg_text, data_cfg)

    # Implementation of Model Training Section
    def model_train_page(self):
        # Creating a new Tkinter window
        self.model_train_window = tk.Toplevel(self.master)
        self.model_train_window.title("Model Training")

        self._create_dataset_preparation_frame()
        self._create_model_train_frame()

    @staticmethod
    def _load_data(target_dir="./MetaHand/tools/yolov7/data/"):
        data_list = []
        for filename in os.listdir(target_dir):
            if filename.endswith(".yaml") and not filename.startswith("hyp"):
                data_list.append(os.path.splitext(filename)[0])
        return data_list

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
            if event.widget == self.image_path_entry:
                event.widget.insert(tk.END, "Please enter the path of training images")
            elif event.widget == self.dataset_name_entry:
                event.widget.insert(tk.END, "Please enter the name of your dataset")
            elif event.widget == self.label_path_entry:
                event.widget.insert(tk.END, "Please enter the path of training labels")

    def train_model(self):
        data_name = self.train_data_var.get()
        model_name = self.train_model_var.get()
        model_yaml_path = f"cfg/training/{model_name}.yaml"
        data_yaml_path = os.path.join("/root/MetaHand/tools/yolov7/data/", f"{data_name}.yaml")
        dnnTest.train_yolov7(proj_name=data_name, data_path=data_yaml_path, cfg_path=model_yaml_path)
        print(f"Model training is finished. The best weights is saved in \
        ./MetaHand/tools/yolov7/runs/train/{data_name}/weights/best.pt")

    def prepare_dataset(self):
        image_path = "./runtime/images"
        label_path = "./runtime/labels"
        if os.path.exists(image_path):
            shutil.rmtree(image_path)
        if os.path.exists(label_path):
            shutil.rmtree(label_path)
        os.makedirs("runtime", exist_ok=True)
        shutil.copytree(self.image_folder_path, image_path)
        shutil.copytree(self.label_folder_path, label_path)
        dataset_name = self.dataset_name_entry.get()
        dataset_dir = dnnTest.prepare_dataset(dataset_name=dataset_name, image_path=image_path, label_path=label_path)

        # Clear the current menu
        menu = self.data_menu['menu']
        menu.delete(0, 'end')

        # Add the new options to the menu
        for option in self._load_data():
            menu.add_command(label=option, command=lambda value=option: self.train_data_var.set(value))
