import os
import shutil
import tkinter as tk
from tkinter import filedialog

from api import DNNTest
from util import update_readonly_textbox

dnnTest = DNNTest("DNNTesting")

CLEAR_LIST = []


class ModelRepairingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_repairing_window = None
        self.model_path = ""
        self.model_repairing_page()

    @staticmethod
    def _load_data(target_dir="./MetaHand/tools/yolov7/data/"):
        data_list = []
        for filename in os.listdir(target_dir):
            if filename.endswith(".yaml") and not filename.startswith("hyp"):
                data_list.append(os.path.splitext(filename)[0])
        return data_list

    def _create_dataset_mutation_page(self, ):
        dataset_preparation_frame = tk.Frame(self.model_repairing_window)
        dataset_preparation_frame.pack(side=tk.LEFT)

        dataset_name_frame = tk.Frame(dataset_preparation_frame)
        dataset_name_frame.pack(side=tk.TOP)
        data_label = tk.Label(dataset_name_frame, text="Select Original Training Dataset: ")
        data_label.pack(side=tk.LEFT)
        self.train_data_var = tk.StringVar()
        cfg_list = self._load_data()
        self.train_data_var.set(cfg_list[0])  # default value
        self.data_menu = tk.OptionMenu(dataset_name_frame, self.train_data_var, *cfg_list)
        self.data_menu.pack(side=tk.LEFT)

        mutate_option_frame = tk.Frame(dataset_preparation_frame)
        mutate_option_frame.pack(side=tk.TOP)
        mutate_label = tk.Label(mutate_option_frame, text="Select Mutation Type: ")
        mutate_label.pack(side=tk.LEFT)
        self.mutate_var = tk.StringVar()
        self.mutate_var.set("ObjectGaussianMutation")  # default value
        self.mutate_menu = tk.OptionMenu(mutate_option_frame, self.mutate_var, "ObjectGaussianMutation",
                                         "BackgroundGaussianMutation")
        self.mutate_menu.pack(side=tk.LEFT)

        def browse_label_path():
            filepath = filedialog.askopenfilename(initialdir="./")
            self.model_path = filepath
            update_readonly_textbox(self.model_path_box, filepath)

        model_path_frame = tk.Frame(dataset_preparation_frame)
        model_path_frame.pack(side=tk.TOP)
        self.model_path_button = tk.Button(model_path_frame, text="Select Original Model",
                                           command=browse_label_path)
        self.model_path_button.pack(side=tk.TOP)
        self.model_path_box = tk.Text(model_path_frame, height=1, width=50)
        self.model_path_box.pack(side=tk.TOP)

        mutate_ratio_frame = tk.Frame(dataset_preparation_frame)
        mutate_ratio_frame.pack(side=tk.TOP)
        self.mutate_ratio_entry: tk.Entry = self.entry_module(frame=mutate_ratio_frame,
                                                              default_entry_text="Enter the mutation ratio (0-1)",
                                                              des="Mutation Ratio", label_width=12, entry_width=30)

        mutate_strength_frame = tk.Frame(dataset_preparation_frame)
        mutate_strength_frame.pack(side=tk.TOP)
        self.mutate_strength_entry: tk.Entry = self.entry_module(frame=mutate_strength_frame,
                                                                 default_entry_text="Enter the mutation strength (e.g., 160)",
                                                                 des="Mutation Strength", label_width=12,
                                                                 entry_width=30)
        model_epoch_frame = tk.Frame(dataset_preparation_frame)
        model_epoch_frame.pack(side=tk.TOP)
        self.epoch_entry: tk.Entry = self.entry_module(frame=model_epoch_frame,
                                                       default_entry_text="Enter the Number of Epoch",
                                                       des="Epoch: ")

        self.dataset_button = tk.Button(dataset_preparation_frame, text="Start Model Repairing",
                                        command=self.repair_model)
        self.dataset_button.pack()

    def entry_module(self, frame, default_entry_text, des, label_width=10, entry_width=40):
        CLEAR_LIST.append(default_entry_text)
        label = tk.Label(frame, width=label_width, text=des)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=entry_width)
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
            if event.widget == self.mutate_ratio_entry:
                event.widget.insert(tk.END, "Enter the mutation ratio (0-1)")
            elif event.widget == self.mutate_strength_entry:
                event.widget.insert(tk.END, "Enter the mutation strength (e.g., 160)")
            elif event.widget == self.epoch_entry:
                event.widget.insert(tk.END, "Enter the Number of Epoch")

    def repair_model(self):
        data_name = self.train_data_var.get()
        mutate_strength = self.mutate_strength_entry.get()
        mutate_ratio = self.mutate_ratio_entry.get().replace(".", "")
        mutate_type = self.mutate_var.get()
        mutate_path = f"/root/MetaHand/tools/yolov7/{data_name}/{mutate_type}/object_gaussian_{mutate_strength}_fixMutRatio_centerXY_{mutate_ratio}"
        model_path = "runtime/weight.pt"
        if os.path.exists(model_path):
            os.remove(model_path)
        os.makedirs("runtime", exist_ok=True)
        if "tools/yolov7/" in self.model_path:
            model_path = "./MetaHand/tools/yolov7/" + self.model_path.split("/tools/yolov7/")[-1]
        else:
            shutil.copy(self.model_path, model_path)
        if not os.path.exists(mutate_path.replace("/root/", "")):
            if mutate_type == "ObjectGaussianMutation":
                _mutate_type = "object"
            else:
                _mutate_type = "background"
            dnnTest.mutate_image("directory", f"/root/MetaHand/tools/yolov7/{data_name}/images/train",
                                 f"/root/MetaHand/tools/yolov7/{data_name}/labels/train",
                                 f"/root/MetaHand/tools/yolov7/{data_name}/{mutate_type}",
                                 _mutate_type, f"{self.mutate_ratio_entry.get()}", f"{mutate_strength[:-1] + '.0'}",
                                 "darknet")
            shutil.move(
                f"MetaHand/tools/yolov7/{data_name}/{mutate_type}/{mutate_type}/object_gaussian_{mutate_strength}_fixMutRatio_centerXY_{mutate_ratio}",
                f"MetaHand/tools/yolov7/{data_name}/{mutate_type}/object_gaussian_{mutate_strength}_fixMutRatio_centerXY_{mutate_ratio}")

        print(f"Start repairing the model.")
        dnnTest.repair_yolov7(
            data_dir=f"/root/MetaHand/tools/yolov7/{data_name}",
            weights_path=os.path.join("/root/", model_path),
            mutate_type=mutate_type,
            mutate_ratio=mutate_ratio,
            mutate_strength=int(mutate_strength),
            num_epoch=int(self.epoch_entry.get())
        )
        if mutate_type == "ObjectGaussianMutation":
            mutate_name = f"object_gaussian_{mutate_strength}_fixMutRatio_centerXY_{mutate_ratio}"
        else:
            mutate_name = f"background_gaussian_{mutate_strength}_fixMutRatio_centerXY_{mutate_ratio}"

        print(f"The new model are stored in ./MetaHand/tools/yolov7/{data_name}_yolov7_{mutate_name}_*")

    # Implementation of Model Training Section
    def model_repairing_page(self):
        # Creating a new Tkinter window
        self.model_repairing_window = tk.Toplevel(self.master)
        self.model_repairing_window.title("Model Repairing")
        self._create_dataset_mutation_page()
        # self._create_model_evaluation_frame()
