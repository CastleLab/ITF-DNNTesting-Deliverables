import tkinter as tk


class ModelEvaluationPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.model_evaluation_window = None
        self.model_evaluation_page()

    # Implementation of Model Evaluation Section
    def model_evaluation_page(self):
        # Creating a new Tkinter window
        self.model_evaluation_window = tk.Toplevel(self.master)
        self.model_evaluation_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.model_evaluation_window)
        create_network_frame.pack(side="left")
