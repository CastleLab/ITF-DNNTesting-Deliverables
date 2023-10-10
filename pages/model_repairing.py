import os
import tkinter as tk

from api import DNNTest

dnnTest = DNNTest("DNNTesting")

CLEAR_LIST = []


class ModelRepairingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_repairing_window = None
        self.model_repairing_page()

    def _create_dataset_mutation_page(self, ):
        dataset_preparation_frame = tk.Frame(self.model_repairing_window)
        dataset_preparation_frame.pack(side=tk.LEFT)

        dataset_name_frame = tk.Frame(dataset_preparation_frame)
        dataset_name_frame.pack(side=tk.TOP)
        self.dataset_name_entry: tk.Entry = self.entry_module(frame=dataset_name_frame,
                                                              default_entry_text="Please enter the name of your dataset",
                                                              des="Dataset name")

        mutate_option_frame = tk.Frame(dataset_preparation_frame)
        mutate_option_frame.pack(side=tk.TOP)
        mutate_label = tk.Label(mutate_option_frame, text="Select Dataset:")
        mutate_label.pack(side=tk.LEFT)
        self.mutate_var = tk.StringVar()
        self.mutate_var.set("ObjectGaussianMutation")  # default value
        self.mutate_menu = tk.OptionMenu(mutate_option_frame, self.mutate_var, "ObjectGaussianMutation",
                                         "BackgroundGaussianMutation")
        self.mutate_menu.pack(side=tk.LEFT)

        mutate_ratio_frame = tk.Frame(dataset_preparation_frame)
        mutate_ratio_frame.pack(side=tk.TOP)
        self.mutate_ratio_entry: tk.Entry = self.entry_module(frame=mutate_ratio_frame,
                                                              default_entry_text="Please enter the mutation ratio (0-1)",
                                                              des="Mutation Ratio")

        mutate_strength_frame = tk.Frame(dataset_preparation_frame)
        mutate_strength_frame.pack(side=tk.TOP)
        self.mutate_strength_entry: tk.Entry = self.entry_module(frame=mutate_strength_frame,
                                                                 default_entry_text="Please enter the mutation strength (e.g., 160)",
                                                                 des="Mutation Strength")

        model_path_frame = tk.Frame(dataset_preparation_frame)
        model_path_frame.pack(side=tk.TOP)
        self.model_path_entry: tk.Entry = self.entry_module(frame=model_path_frame,
                                                            default_entry_text="Please enter the path of model to be evaluated",
                                                            des="Model Path")

        self.dataset_button = tk.Button(dataset_preparation_frame, text="Start Model Evaluation",
                                        command=self.repair_model)
        self.dataset_button.pack()

    def entry_module(self, frame, default_entry_text, des):
        CLEAR_LIST.append(default_entry_text)
        label = tk.Label(frame, width=10, text=des)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=40)
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
            if event.widget == self.dataset_name_entry:
                event.widget.insert(tk.END, "Please enter the name of your dataset")
            elif event.widget == self.mutate_ratio_entry:
                event.widget.insert(tk.END, "Please enter the mutation ratio (0-1)")
            elif event.widget == self.mutate_strength_entry:
                event.widget.insert(tk.END, "Please enter the mutation strength (e.g., 160)")
            elif event.widget == self.model_path_entry:
                event.widget.insert(tk.END, "Please enter the path of model to be evaluated")

    def repair_model(self):
        data_name = self.dataset_name_entry.get()
        mutate_strength = self.mutate_strength_entry.get()
        mutate_ratio = self.mutate_ratio_entry.get().replace(".", "")
        mutate_type = self.mutate_var.get()
        model_path = self.model_path_entry.get()
        dnnTest.repair_yolov7(
            data_dir=f"/root/MetaHand/tools/yolov7/{data_name}",
            weights_path=os.path.join("/root/", model_path),
            mutate_type=mutate_type,
            mutate_ratio=mutate_ratio,
            mutate_strength=int(mutate_strength)
        )

    # Implementation of Model Training Section
    def model_repairing_page(self):
        # Creating a new Tkinter window
        self.model_repairing_window = tk.Toplevel(self.master)
        self.model_repairing_window.title("Model Repairing")
        self._create_dataset_mutation_page()
        # self._create_model_evaluation_frame()
