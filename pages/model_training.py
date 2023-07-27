import os
import tkinter as tk
import yaml
from util import string_is_float
from api import DNNTest

dnnTest = DNNTest("DNNTesting")

CLEAR_LIST = []


class ModelTrainingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_train_window = None
        self.model_train_page()

    # Implementation of Model Training Section
    def model_train_page(self):
        # Creating a new Tkinter window
        self.model_train_window = tk.Toplevel(self.master)
        self.model_train_window.title("Detecting Numerical Bugs in Neural Networks")

        dataset_preparation_frame = tk.Frame(self.model_train_window)
        dataset_preparation_frame.pack(side=tk.LEFT)

        image_selection_frame = tk.Frame(dataset_preparation_frame)
        image_selection_frame.pack(side=tk.TOP)
        self.image_path_entry: tk.Entry = self.entry_module(frame=image_selection_frame,
                                                  default_entry_text="Please enter the path of training images",
                                                  des="Image path")

        label_selection_frame = tk.Frame(dataset_preparation_frame)
        label_selection_frame.pack(side=tk.TOP)
        self.label_path_entry: tk.Entry = self.entry_module(frame=label_selection_frame,
                                                  default_entry_text="Please enter the path of training labels",
                                                  des="Label path")

        dataset_name_frame = tk.Frame(dataset_preparation_frame)
        dataset_name_frame.pack(side=tk.TOP)
        self.dataset_name_entry: tk.Entry = self.entry_module(frame=dataset_name_frame,
                                                            default_entry_text="Please enter the name of your dataset",
                                                            des="Dataset name")

        self.dataset_button = tk.Button(dataset_preparation_frame, text="Prepare Dataset",
                                             command=self.prepare_dataset)
        self.dataset_button.pack()

        # Creating the "Selecting Dataset" section
        model_train_frame = tk.Frame(self.model_train_window)
        model_train_frame.pack(side=tk.LEFT)

        self.train_data_var = tk.StringVar()
        network_list = self._load_data()
        self.train_data_var.set(network_list[0])  # default value
        data_menu = tk.OptionMenu(model_train_frame, self.train_data_var, *network_list)
        data_menu.pack()

        def show_data_cfg():
            with open(os.path.join("./MetaHand/tools/yolov7/data/", f"{self.train_data_var.get()}.yaml"), "r") as file:
                data_hyp = yaml.load(file, Loader=yaml.FullLoader)

            self.model_train_hyp_entry = tk.Text(model_train_frame, height=5, width=50)
            self.model_train_hyp_entry.insert(
                "1.0",
                f"train: {data_hyp['train']}\n"
                f"val: {data_hyp['val']}\n"
                f"test: {data_hyp['test']}"
            )
            self.model_train_hyp_entry.pack()
            self.model_train_hyp_entry.configure(state=tk.DISABLED)

        show_data_cfg()

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

    def prepare_dataset(self):
        image_path = self.image_path_entry.get()
        label_path = self.label_path_entry.get()
        dataset_name = self.dataset_name_entry.get()
        dataset_dir = dnnTest.prepare_dataset(dataset_name=dataset_name, image_path=image_path, label_path=label_path)
        print(dataset_dir)
