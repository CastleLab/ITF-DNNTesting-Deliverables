import tkinter as tk


class ModelRepairingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_repair_window = None
        self.model_repair_page()

    # Implementation of Model Repairing Section
    def model_repair_page(self):
        # Creating a new Tkinter window
        self.model_repair_window = tk.Toplevel(self.master)
        self.model_repair_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.model_repair_window)
        create_network_frame.pack(side="left")
