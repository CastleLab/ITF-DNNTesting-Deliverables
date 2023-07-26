import tkinter as tk


class ImageMutationPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.image_mutation_window = None
        self.image_mutation_page()

    # Implementation of Image Mutation Section
    def image_mutation_page(self):
        # Creating a new Tkinter window
        self.image_mutation_window = tk.Toplevel(self.master)
        self.image_mutation_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.image_mutation_window)
        create_network_frame.pack(side="left")
