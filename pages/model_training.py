import tkinter as tk
import os
import yaml


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

        # Creating the "Selecting Dataset" section
        model_train_frame = tk.Frame(self.model_train_window)
        model_train_frame.pack(side="left")

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
